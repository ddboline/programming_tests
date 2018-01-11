#![feature(proc_macro, specialization)]

extern crate pyo3;
use pyo3::{py, Python, PyResult, PyModule, PyString};

// add bindings to the generated python module
// N.B: names: "libhello" must be the name of the `.so` or `.pyd` file

/// Module documentation string
#[py::modinit(hello)]
fn init_module(py: Python, m: &PyModule) -> PyResult<()> {

    // pyo3 aware function. All of our python interface could be declared
    // in a separate module.
    // Note that the `#[pyfn()]` annotation automatically converts the arguments from
    // Python objects to Rust values; and the Rust return value back into a Python object.
    #[pyfn(m, "run_rust_func")]
    fn run(name: &PyString) -> PyResult<()> {
        println!("Rust says: Hello {} of Python!", name);
        Ok(())
    }

    Ok(())
}
