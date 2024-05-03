"use strict";
// Copyright 2020 Google Inc. Use of this source code is governed by an
// MIT-style license that can be found in the LICENSE file or at
// https://opensource.org/licenses/MIT.
Object.defineProperty(exports, "__esModule", { value: true });
exports.expectEqualWithHashCode = exports.expectEqualIgnoringWhitespace = exports.expectEqualPaths = exports.expectObservableToError = void 0;
/**
 * Subscribes to `observable` and asserts that it errors with the expected
 * `errorMessage`. Calls `done()` to complete the spec.
 */
function expectObservableToError(observable, errorMessage, done) {
    observable.subscribe({
        next: () => {
            throw new Error('expected error');
        },
        error: error => {
            expect(error.message).toBe(errorMessage);
            done();
        },
        complete: () => {
            throw new Error('expected error');
        },
    });
}
exports.expectObservableToError = expectObservableToError;
/**
 * Asserts that the `actual` path is equal to the `expected` one, accounting for
 * OS differences.
 */
function expectEqualPaths(actual, expected) {
    if (process.platform === 'win32') {
        expect(actual.toLowerCase()).toBe(expected.toLowerCase());
    }
    else {
        expect(actual).toBe(expected);
    }
}
exports.expectEqualPaths = expectEqualPaths;
/**
 * Asserts that `string1` is equal to `string2`, ignoring all whitespace in
 * either string.
 */
function expectEqualIgnoringWhitespace(string1, string2) {
    function strip(str) {
        return str.replace(/\s+/g, '');
    }
    expect(strip(string1)).toBe(strip(string2));
}
exports.expectEqualIgnoringWhitespace = expectEqualIgnoringWhitespace;
/**
 * Asserts that `val1` and `val2` are equal and have the same hashcode.
 */
function expectEqualWithHashCode(val1, val2) {
    expect(val1.equals(val2)).toBe(true);
    expect(val1.hashCode()).toBe(val2.hashCode());
}
exports.expectEqualWithHashCode = expectEqualWithHashCode;
//# sourceMappingURL=utils.js.map