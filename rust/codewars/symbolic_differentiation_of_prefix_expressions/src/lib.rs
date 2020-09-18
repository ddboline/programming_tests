/// Steps:
/// 1. parse from string to Expr
/// 2. differentiate Expr to new Expr
/// 3. simplify Expr
/// 4. print Expr
use std::fmt;
use std::str::FromStr;

fn diff(expr: &str) -> String {
    let e = Expr::parse(expr);
    println!("expr {:?}", e);
    let d = e.diff();
    println!("diff {:?}", d);
    let d = d.simplify();
    println!("simp0 {:?}", d);
    let d = d.simplify();
    println!("simp1 {:?}", d);
    d.to_string()
}

fn repr(expr: &str) -> String {
    let s = Expr::parse(expr);
    s.to_string()
}

#[derive(Clone, Debug)]
enum Expr {
    Arg(Arg),
    Func {
        func: Func,
        arg: Box<Expr>,
    },
    Op {
        op: Op,
        arg1: Box<Expr>,
        arg2: Box<Expr>,
    },
}

impl fmt::Display for Expr {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Arg(a) => write!(f, "{}", a),
            Self::Func { func, arg } => write!(f, "({} {})", func, arg),
            Self::Op { op, arg1, arg2 } => write!(f, "({} {} {})", op, arg1, arg2),
        }
    }
}

impl Expr {
    fn parse(s: &str) -> Self {
        let mut iter = s.split_whitespace();
        Self::parse_internal(&mut iter).unwrap()
    }

    fn parse_internal<'a, T: Iterator<Item = &'a str>>(iter: &mut T) -> Option<Self> {
        if let Some(s) = iter.next() {
            if s.starts_with("(") {
                if let Ok(func) = s[1..].parse::<Func>() {
                    Some(Self::Func {
                        func,
                        arg: Box::new(Self::parse_internal(iter).unwrap()),
                    })
                } else if let Ok(op) = s[1..].parse::<Op>() {
                    Some(Self::Op {
                        op,
                        arg1: Box::new(Self::parse_internal(iter).unwrap()),
                        arg2: Box::new(Self::parse_internal(iter).unwrap()),
                    })
                } else {
                    panic!("This shouldn't happen...")
                }
            } else if s.ends_with(")") {
                let end = s.find(')').unwrap();
                Some(Self::Arg(s[..end].parse::<Arg>().unwrap()))
            } else {
                Some(Self::Arg(s.parse::<Arg>().unwrap()))
            }
        } else {
            None
        }
    }

    fn simplify(self) -> Self {
        match self {
            Self::Arg(a) => Self::Arg(a),
            Self::Func { func, arg } => Self::Func {
                func,
                arg: Box::new(arg.simplify()),
            },
            Self::Op { op, arg1, arg2 } => {
                if !arg1.contains_variable() && !arg2.contains_variable() {
                    let val1 = match arg1.simplify() {
                        Self::Arg(Arg::Int(i)) => i as f64,
                        Self::Arg(Arg::Float(f)) => f,
                        _ => unreachable!(),
                    };
                    let val2 = match arg2.clone().simplify() {
                        Self::Arg(Arg::Int(i)) => i as f64,
                        Self::Arg(Arg::Float(f)) => f,
                        _ => unreachable!(),
                    };
                    let val = match op {
                        Op::Add => val1 + val2,
                        Op::Sub => val1 - val2,
                        Op::Mul => val1 * val2,
                        Op::Div => val1 / val2,
                        Op::Pow => val1.powf(val2),
                    };
                    Self::Arg(Arg::Float(val))
                } else if arg1.contains_variable() {
                    let val2 = match arg2.simplify() {
                        Self::Arg(Arg::Int(i)) => i as f64,
                        Self::Arg(Arg::Float(f)) => f,
                        _ => unreachable!(),
                    };
                    if val2 == 0.0 {
                        match op {
                            Op::Add | Op::Sub => arg1.simplify(),
                            Op::Mul => Self::Arg(Arg::Int(0)),
                            Op::Div => unreachable!(),
                            Op::Pow => Self::Arg(Arg::Int(1)),
                        }
                    } else if val2 == 1.0 {
                        match op {
                            Op::Mul | Op::Div => arg1.simplify(),
                            Op::Pow => arg1.simplify(),
                            _ => Self::Op {
                                op,
                                arg1: Box::new(arg1.simplify()),
                                arg2: Box::new(Self::Arg(Arg::Float(val2))),
                            },
                        }
                    } else {
                        Self::Op {
                            op,
                            arg1: Box::new(arg1.simplify()),
                            arg2: Box::new(Self::Arg(Arg::Float(val2))),
                        }
                    }
                } else if arg2.contains_variable() {
                    let val1 = match arg1.simplify() {
                        Self::Arg(Arg::Int(i)) => i as f64,
                        Self::Arg(Arg::Float(f)) => f,
                        _ => unreachable!(),
                    };
                    if val1 == 0.0 {
                        match op {
                            Op::Add | Op::Sub => arg2.simplify(),
                            Op::Mul => Self::Arg(Arg::Int(0)),
                            Op::Div => unreachable!(),
                            Op::Pow => Self::Arg(Arg::Int(1)),
                        }
                    } else if val1 == 1.0 {
                        match op {
                            Op::Mul | Op::Div => arg2.simplify(),
                            Op::Pow => arg2.simplify(),
                            _ => Self::Op {
                                op,
                                arg1: Box::new(Self::Arg(Arg::Float(val1))),
                                arg2: Box::new(arg2.simplify()),
                            },
                        }
                    } else {
                        Self::Op {
                            op,
                            arg1: Box::new(Self::Arg(Arg::Float(val1))),
                            arg2: Box::new(arg2.simplify()),
                        }
                    }
                } else {
                    Self::Op {
                        op,
                        arg1: Box::new(arg1.simplify()),
                        arg2: Box::new(arg2.simplify()),
                    }
                }
            }
        }
    }

    fn contains_variable(&self) -> bool {
        match self {
            Self::Arg(Arg::Int(_)) | Self::Arg(Arg::Float(_)) => return false,
            Self::Arg(Arg::Variable) => true,
            Self::Func { func: _, arg } => arg.contains_variable(),
            Self::Op { op: _, arg1, arg2 } => {
                if arg1.contains_variable() || arg2.contains_variable() {
                    true
                } else {
                    false
                }
            }
        }
    }

    fn diff(&self) -> Self {
        match self {
            Self::Arg(Arg::Int(_)) | Self::Arg(Arg::Float(_)) => Self::Arg(Arg::Int(0)),
            Self::Arg(Arg::Variable) => Self::Arg(Arg::Int(1)),
            Self::Func { func, arg } => match func {
                Func::Cos => Self::Op {
                    op: Op::Mul,
                    arg1: Box::new(arg.diff()),
                    arg2: Box::new(Self::Op {
                        op: Op::Mul,
                        arg1: Box::new(Self::Arg(Arg::Int(-1))),
                        arg2: {
                            Box::new(Self::Func {
                                func: Func::Sin,
                                arg: arg.clone(),
                            })
                        },
                    }),
                },
                Func::Sin => Self::Op {
                    op: Op::Mul,
                    arg1: Box::new(arg.diff()),
                    arg2: Box::new(Self::Func {
                        func: Func::Cos,
                        arg: arg.clone(),
                    }),
                },
                Func::Tan => Self::Op {
                    op: Op::Mul,
                    arg1: Box::new(arg.diff()),
                    arg2: Box::new(Self::Op {
                        op: Op::Div,
                        arg1: Box::new(Self::Arg(Arg::Int(1))),
                        arg2: Box::new(Self::Op {
                            op: Op::Pow,
                            arg1: Box::new(Self::Func {
                                func: Func::Cos,
                                arg: arg.clone(),
                            }),
                            arg2: Box::new(Self::Arg(Arg::Int(2))),
                        }),
                    }),
                },
                Func::Exp => Self::Op {
                    op: Op::Mul,
                    arg1: Box::new(arg.diff()),
                    arg2: Box::new(Self::Func {
                        func: Func::Exp,
                        arg: arg.clone(),
                    }),
                },
                Func::Ln => Self::Op {
                    op: Op::Mul,
                    arg1: Box::new(arg.diff()),
                    arg2: Box::new(Self::Op {
                        op: Op::Div,
                        arg1: Box::new(Self::Arg(Arg::Int(1))),
                        arg2: arg.clone(),
                    }),
                },
            },
            Self::Op { op, arg1, arg2 } => match op {
                Op::Add => Self::Op {
                    op: Op::Add,
                    arg1: Box::new(arg1.diff()),
                    arg2: Box::new(arg2.diff()),
                },
                Op::Sub => Self::Op {
                    op: Op::Sub,
                    arg1: Box::new(arg1.diff()),
                    arg2: Box::new(arg2.diff()),
                },
                Op::Mul => Self::Op {
                    op: Op::Add,
                    arg1: Box::new(Self::Op {
                        op: Op::Mul,
                        arg1: Box::new(arg1.diff()),
                        arg2: arg2.clone(),
                    }),
                    arg2: Box::new(Self::Op {
                        op: Op::Mul,
                        arg1: arg1.clone(),
                        arg2: Box::new(arg2.diff()),
                    }),
                },
                Op::Div => Self::Op {
                    op: Op::Mul,
                    arg1: arg1.clone(),
                    arg2: Box::new(Self::Op {
                        op: Op::Pow,
                        arg1: arg2.clone(),
                        arg2: Box::new(Self::Arg(Arg::Int(-1))),
                    }),
                }
                .diff(),
                Op::Pow => {
                    if arg1.contains_variable() {
                        if arg2.contains_variable() {
                            panic!("Thar be dragons")
                        } else {
                            Self::Op {
                                op: Op::Mul,
                                arg1: Box::new(arg1.diff()),
                                arg2: Box::new(Self::Op {
                                    op: Op::Mul,
                                    arg1: arg2.clone(),
                                    arg2: Box::new(Self::Op {
                                        op: Op::Pow,
                                        arg1: arg1.clone(),
                                        arg2: Box::new(Self::Op {
                                            op: Op::Sub,
                                            arg1: arg2.clone(),
                                            arg2: Box::new(Self::Arg(Arg::Int(1))),
                                        }),
                                    }),
                                }),
                            }
                        }
                    } else {
                        Self::Arg(Arg::Int(0))
                    }
                }
            },
        }
    }
}

#[derive(Clone, Copy, Debug)]
enum Arg {
    Variable,
    Int(i64),
    Float(f64),
}

impl fmt::Display for Arg {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Arg::Variable => write!(f, "x"),
            Arg::Int(x) => write!(f, "{}", x),
            Arg::Float(x) => write!(f, "{}", x),
        }
    }
}

impl FromStr for Arg {
    type Err = ();
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        if s.contains(" ") || s.contains("(") || s.contains(")") {
            Err(())
        } else if let Ok(i) = s.parse::<i64>() {
            Ok(Arg::Int(i))
        } else if let Ok(f) = s.parse::<f64>() {
            Ok(Arg::Float(f))
        } else if s == "x" {
            Ok(Arg::Variable)
        } else {
            Err(())
        }
    }
}

#[derive(Clone, Copy, Debug)]
enum Func {
    Cos,
    Sin,
    Tan,
    Exp,
    Ln,
}

#[derive(Clone, Copy, Debug)]
enum Op {
    Add,
    Sub,
    Mul,
    Div,
    Pow,
}

impl FromStr for Func {
    type Err = ();
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "cos" => Ok(Self::Cos),
            "sin" => Ok(Self::Sin),
            "tan" => Ok(Self::Tan),
            "exp" => Ok(Self::Exp),
            "ln" => Ok(Self::Ln),
            _ => Err(()),
        }
    }
}

impl FromStr for Op {
    type Err = ();
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "+" => Ok(Self::Add),
            "-" => Ok(Self::Sub),
            "*" => Ok(Self::Mul),
            "/" => Ok(Self::Div),
            "^" => Ok(Self::Pow),
            _ => Err(()),
        }
    }
}

impl From<&Func> for &'static str {
    fn from(item: &Func) -> Self {
        match item {
            Func::Cos => "cos",
            Func::Sin => "sin",
            Func::Tan => "tan",
            Func::Exp => "exp",
            Func::Ln => "ln",
        }
    }
}

impl From<&Op> for &'static str {
    fn from(item: &Op) -> Self {
        match item {
            Op::Add => "+",
            Op::Sub => "-",
            Op::Mul => "*",
            Op::Div => "/",
            Op::Pow => "^",
        }
    }
}

impl fmt::Display for Op {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let s: &'static str = self.into();
        write!(f, "{}", s)
    }
}

impl fmt::Display for Func {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let s: &'static str = self.into();
        write!(f, "{}", s)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parser() {
        for x in &[
            "5",
            "x",
            "(+ x x)",
            "(* x 2)",
            "(cos x)",
            "(cos (+ x 1))",
            "(* 2 (+ 1 (^ (tan (* 2 (cos (+ x 1)))) 2)))",
        ] {
            assert_eq!(&repr(x), x);
        }
    }

    #[test]
    fn test_fixed() {
        assert_eq!(diff("5"), "0");
        assert_eq!(diff("x"), "1");
        assert_eq!(diff("5"), "0");
        assert_eq!(diff("(+ x x)"), "2");
        assert_eq!(diff("(- x x)"), "0");
        assert_eq!(diff("(* x 2)"), "2");
        assert_eq!(diff("(/ x 2)"), "0.5");
        assert_eq!(diff("(^ x 2)"), "(* 2 x)");
        assert_eq!(diff("(cos x)"), "(* -1 (sin x))");
        assert_eq!(diff("(sin x)"), "(cos x)");
        assert_eq!(diff("(tan x)"), "(/ 1 (^ (cos x) 2))");
        assert_eq!(diff("(exp x)"), "(exp x)");
        assert_eq!(diff("(ln x)"), "(/ 1 x)");
        assert_eq!(diff("(+ x (+ x x))"), "3");
        assert_eq!(diff("(- (+ x x) x)"), "1");
        assert_eq!(diff("(* 2 (+ x 2))"), "2");
        assert_eq!(diff("(/ 2 (+ 1 x))"), "(/ -2 (^ (+ 1 x) 2))");
        assert_eq!(diff("(cos (+ x 1))"), "(* -1 (sin (+ x 1)))");

        let result = diff("(cos (* 2 x))");
        assert!(
            result == "(* 2 (* -1 (sin (* 2 x))))"
                || result == "(* -2 (sin (* 2 x)))"
                || result == "(* (* -1 (sin (* 2 x))) 2)"
        );

        assert_eq!(diff("(sin (+ x 1))"), "(cos (+ x 1))");
        assert_eq!(diff("(sin (* 2 x))"), "(* 2 (cos (* 2 x)))");
        assert_eq!(diff("(tan (* 2 x))"), "(* 2 (+ 1 (^ (tan (* 2 x)) 2)))");
        assert_eq!(diff("(exp (* 2 x))"), "(* 2 (exp (* 2 x)))");
        assert_eq!(diff(&diff("(sin x)")), "(* -1 (sin x))");
        assert_eq!(diff(&diff("(exp x)")), "(exp x)");

        let result = diff(&diff("(^ x 3)"));
        assert!(result == "(* 3 (* 2 x))" || result == "(* 6 x)");
    }
}
