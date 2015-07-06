class Muslim:
    def performsMuslimRitual(self):
        return
 
class MuslimFemale(Muslim):
    def performsMuslimRitual(self):
        print("Muslim girl performs Muslim ritual.")
 
class Hindu:
    def performsHinduRitual(self):
        return
 
class HinduFemale(Hindu):
    def performsHinduRitual(self):
        print("Hindu girl performs Hindu ritual.")
 
class MuslimRitual:
    def carryOutRitual(self, muslim):
        print("On with the Muslim rituals!")
        muslim.performsMuslimRitual()
 
class MuslimAdapter(Muslim):
    def __init__(self, h):
        self.hindu = h
    def performsMuslimRitual(self):
        self.hindu.performsHinduRitual()

if __name__ == '__main__':
    hinduGirl = HinduFemale()
    muslimGirl = MuslimFemale()
    muslimRitual = MuslimRitual()
    #muslimRitual.carryOutRitual(hinduGirl)
    adaptedHindu = MuslimAdapter(hinduGirl)
 
    muslimRitual.carryOutRitual(muslimGirl)
    muslimRitual.carryOutRitual(adaptedHindu)
