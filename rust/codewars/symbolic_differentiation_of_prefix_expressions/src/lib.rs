/// Steps:
/// 1. parse from string to Expr
/// 2. differentiate Expr to new Expr
/// 3. simplify Expr
/// 4. print Expr

use std::fmt;
use std::str::FromStr;

fn diff(expr: &str) -> String {
    expr.to_string()
}

#[derive(Clone)]
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

impl Expr {
    fn parse(s: &str) -> Self {
        let begin = s.find('(');
        let end = s.find(')');

        Self::Arg(Arg::Int(0))
    }

    fn diff(&self) -> Self {
        match self {
            Self::Arg(Arg::Int(_)) => Self::Arg(Arg::Int(0)),
            Self::Arg(Arg::Float(_)) => Self::Arg(Arg::Int(0)),
            Self::Arg(Arg::Symbol(s)) => Self::Arg(Arg::Int(1)),
            Self::Func { func, arg } => {
                match func {
                    Func::Cos => Self::Op {
                        op: Op::Mul,
                        arg1: Box::new(arg.diff()),
                        arg2: Box::new(Self::Op {
                            op: Op::Mul,
                            arg1: Box::new(Self::Arg(Arg::Int(-1))),
                            arg2: Box::new(Self::Func {
                                func: Func::Sin,
                                arg: arg.clone(),
                            }),
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
                };
                Self::Arg(Arg::Int(0))
            }
            Self::Op { op, arg1, arg2 } => {
                match op {
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
                        arg1: Box::new(
                            Self::Op {
                                op: Op::Mul,
                                arg1: Box::new(arg1.diff()),
                                arg2: arg2.clone(),
                            }
                        ),
                        arg2: Box::new(
                            Self::Op {
                                op: Op::Mul,
                                arg1: arg1.clone(),
                                arg2: Box::new(arg2.diff()),
                            }
                        )
                    },
                    Op::Div => Self::Op {
                        op: Op::Mul,
                        arg1: arg1.clone(),
                        arg2: Box::new(
                            Self::Op {
                                op: Op::Pow,
                                arg1: arg2.clone(),
                                arg2: Box::new(Self::Arg(Arg::Int(-1))),
                            }
                        )
                    }.diff(),
                    Op::Pow => Self::Op {
                        op: Op::Mul,
                        arg1: Box::new(
                            Self::Op {
                                op: Op::Mul,
                                arg1: Box::new(arg1.diff()),
                                arg2: arg2.clone(),
                            }
                        ),
                        arg2: Box::new(
                            Self::Op {
                                op: Op::Add,
                                arg1: arg2.clone(),
                                arg2: Box::new(Self::Arg(Arg::Int(-1))),
                            }
                        ),
                    },
                }
            }
        };
        Expr::Arg(Arg::Int(0))
    }
}

#[derive(Clone)]
enum Arg {
    Symbol(String),
    Int(i64),
    Float(f64),
}

#[derive(Clone, Copy)]
enum Func {
    Cos,
    Sin,
    Tan,
    Exp,
    Ln,
}

#[derive(Clone, Copy)]
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
        assert_eq!(diff("(tan x)"), "(+ 1 (^ (tan x) 2))");
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
