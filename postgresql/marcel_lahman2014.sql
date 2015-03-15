-- create marcel projection data source using 3 previous years
-- of data, excluding pitchers.
-- 
-- note: this exclusion method risks removing batters who have pitched.
--       instead, we should look for players with more
--       PA than batters faced.
create or replace view
    marcel_batting
as (
    select
        b.playerid
        , (case when m.birthmonth < 7
                then (b.yearid - m.birthyear)
                else (b.yearid - m.birthyear - 1)
           end) age
        , b.yearid
        , sum(g) g
        , sum(ab) ab
        , sum(r) r
        , sum(h) h
        , sum(2b) 2b
        , sum(3b) 3b
        , sum(hr) hr
        , sum(rbi) rbi
        , sum(sb) sb
        , sum(cs) cs
        , sum(bb) bb
        , sum(so) so
        , sum(ibb) ibb
        , sum(hbp) hbp
        , sum(sh) sh
        , sum(sf) sf
        , sum(gidp) gidp
        , sum(ab) + sum(bb) + sum(hbp) + sum(sf) + sum(sh) pa
    from
        batting b
    inner join
        master m
        on m.playerid = b.playerid
    where
        b.playerid in (
            select
                playerid
            from
                batting
            where
                yearid between 2001 and 2003
            except
            select
                playerid
            from
                pitching
            where
                yearid between 2001 and 2003
        )
        and b.yearid between 2001 and 2003
    group by
        b.yearid
        , b.playerid
        , m.birthmonth
        , m.birthyear
)
;
 
-- calculate league rates for components per plate appearance
-- for each of past 3 years (e.g., HR/PA)
create or replace view
    marcel_batting_lgavg
as (    
    select
        yearid
        , sum(pa) lgPA
        , sum(ab) / sum(pa) lgAB
        , sum(rbi) / sum(pa) lgRBI
        , sum(r) / sum(pa) lgR
        , sum(h) / sum(pa) lgH
        , sum(2b) / sum(pa) lg2B
        , sum(3b) / sum(pa) lg3B
        , sum(hr) / sum(pa) lgHR
        , sum(sb) / sum(pa) lgSB
        , sum(cs) / sum(pa) lgCS
        , sum(bb) / sum(pa) lgBB
        , sum(ibb) / sum(pa) lgIBB
        , sum(hbp) / sum(pa) lgHBP
        , sum(sh) / sum(pa) lgSH
        , sum(sf) / sum(pa) lgSF
        , sum(gidp) / sum(pa) lgGIDP
    from
       marcel_batting
    where
       yearid between 2001 and 2003
    group by
       yearid
)
;
 
-- weight player components using 5/4/3 method
create or replace view
    marcel_batting_weighted_player_components
as (
    select
        mb.playerid
        , 5 * mb.pa + 4 * coalesce(mb_1y.pa, 0) + 3 * coalesce(mb_2y.pa, 0) wPA
        , 5 * mb.hr + 4 * coalesce(mb_1y.hr, 0) + 3 * coalesce(mb_2y.hr, 0) wHR
    from
        marcel_batting mb
    left join
        (select * from marcel_batting where yearid=2002) mb_1y
        on mb_1y.playerid = mb.playerid
    left join
        (select * from marcel_batting where yearid=2001) mb_2y
        on mb_2y.playerid = mb.playerid
    where
        mb.yearid = 2003
)
;
 
-- project PA for players
create or replace view
    marcel_batting_projected_pa
as (
    select
        mb.playerid
        , round( (mb.pa * .5) + (coalesce(mb_1y.pa, 0) * .1) + 200 ) pa
    from
        marcel_batting mb
    left join
        (select playerid, pa from marcel_batting where yearid=2002) mb_1y
        on mb_1y.playerid = mb.playerid
    where
        mb.yearid = 2003
)
;
 
-- calculate league mean component values
create or replace view
    marcel_batting_player_lgmeans
as (
    with lgavg as
        ( select * from marcel_batting_lgavg )
    select
        mb.playerid
        , round(
            (
                ((5 * mb.pa * (select lgHR from lgavg where yearid=mb.yearid))
                  + (4 * coalesce(mb_1y.pa, 0) * (select lgHR from lgavg where yearid=2002))
                  + (3 * coalesce(mb_2y.pa, 0) * (select lgHR from lgavg where yearid=2001)))
                * 1200
            ) / wpc.wPA, 1) lgmHR
    from
        marcel_batting mb
    inner join
        marcel_batting_lgavg lgavg on lgavg.yearid = mb.yearid
    inner join
        marcel_batting_weighted_player_components wpc
        on wpc.playerid = mb.playerid
    left join
        (select playerid, pa from marcel_batting where yearid=2002) mb_1y
        on mb_1y.playerid = mb.playerid
    left join
        (select playerid, pa from marcel_batting where yearid=2001) mb_2y
        on mb_2y.playerid = mb.playerid
    where
        mb.yearid = 2003
        and wpc.wPA > 0
)
;
 
create or replace view
    marcel_batting_ageinfo
as (
    select
        playerid
        , max(age) age
        , (
            case when max(age) < 29 then 1 + (max(age) - 29) * 0.006
                 else 1 + (max(age) - 29) * 0.003
            end
        ) wAge
    from
        marcel_batting
    group by
        playerid
)
;
 
-- calculate expected rates for components, project
create or replace view marcel_batting_projections
as (
    select
        wpc.playerid
        , 1 + ageinfo.age age
        , round(wpc.wPA / (wpc.wPA + 1200), 2) relibability
        , round(((wpc.wHR + lgmeans.lgmHR) / (wpc.wPA + 1200)) * ppa.pa * ageinfo.wAge) hr
    from
        marcel_batting_weighted_player_components wpc
    inner join
        marcel_batting_ageinfo ageinfo
        on ageinfo.playerid = wpc.playerid
    inner join
        marcel_batting_player_lgmeans lgmeans
        on lgmeans.playerid = wpc.playerid
    inner join
        marcel_batting_projected_pa ppa
        on ppa.playerid = wpc.playerid
)
;