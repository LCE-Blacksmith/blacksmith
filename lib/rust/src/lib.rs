//! Minecraft legacy console edition mod loader/modding framework 
#![feature(c_variadic)]

use std::{marker::PhantomData, os::raw::c_void};

use crate::hooks::Hook;

mod sys;

pub mod hooks;

fn callback<T: Hook>(callback: T::Callback) -> unsafe extern "C" fn(u32, ...) -> *mut c_void {
    fn v() {}
}

unsafe extern "C" fn variadic_wrapper<H: Hook>(first: u32, mut args: ...) -> *mut c_void {
    const CALLBACK: H::Callback = ...;
    unsafe {H::call(CALLBACK, &mut args.as_va_list())}
}

/// A zero-cost abstraction to prevent adding hooks after initialization.
pub struct InitCtx(PhantomData<*const ()>);

impl InitCtx {
    pub fn hook<T: Hook>(&self, hook: T, callback: T::Callback) {
        unsafe {
            sys::blacksmith_hook(T::VALUE, Some());
        }
    }
}

#[unsafe(no_mangle)]
fn __blacksmith_mod_init(blacksmith_version: u32) {

}
