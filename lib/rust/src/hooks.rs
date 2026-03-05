//! Hooks for blacksmith
use std::ffi::{VaList, c_void};

/// A hook. Unsafe because the compiler can't validate the requirements of Callback.
pub unsafe trait Hook {
    type Callback;
    const VALUE: u32;

    /// Given the callback and a reference to a `VaList`, extract the arguments
    /// and invoke the callback. Returns the callback's result.
    unsafe fn call(callback: Self::Callback, args: &mut VaList) -> *mut c_void;
}