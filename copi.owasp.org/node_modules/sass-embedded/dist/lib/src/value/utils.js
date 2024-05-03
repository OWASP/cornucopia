"use strict";
// Copyright 2021 Google Inc. Use of this source code is governed by an
// MIT-style license that can be found in the LICENSE file or at
// https://opensource.org/licenses/MIT.
Object.defineProperty(exports, "__esModule", { value: true });
exports.positiveMod = exports.fuzzyAssertInRange = exports.fuzzyInRange = exports.fuzzyRound = exports.fuzzyAsInt = exports.fuzzyIsInt = exports.fuzzyGreaterThanOrEquals = exports.fuzzyGreaterThan = exports.fuzzyLessThanOrEquals = exports.fuzzyLessThan = exports.fuzzyHashCode = exports.fuzzyEquals = exports.precision = void 0;
const immutable_1 = require("immutable");
const utils_1 = require("../utils");
/** The precision of Sass numbers. */
exports.precision = 10;
// The max distance two Sass numbers can be from each another before they're
// considered different.
//
// Uses ** instead of Math.pow() for constant folding.
const epsilon = 10 ** (-exports.precision - 1);
/** Whether `num1` and `num2` are equal within `epsilon`. */
function fuzzyEquals(num1, num2) {
    return Math.abs(num1 - num2) < epsilon;
}
exports.fuzzyEquals = fuzzyEquals;
/**
 * Returns a hash code for `num`.
 *
 * Two numbers that `fuzzyEquals` each other must have the same hash code.
 */
function fuzzyHashCode(num) {
    return !isFinite(num) || isNaN(num)
        ? (0, immutable_1.hash)(num)
        : (0, immutable_1.hash)(Math.round(num / epsilon));
}
exports.fuzzyHashCode = fuzzyHashCode;
/** Whether `num1` < `num2`, within `epsilon`. */
function fuzzyLessThan(num1, num2) {
    return num1 < num2 && !fuzzyEquals(num1, num2);
}
exports.fuzzyLessThan = fuzzyLessThan;
/** Whether `num1` <= `num2`, within `epsilon`. */
function fuzzyLessThanOrEquals(num1, num2) {
    return num1 < num2 || fuzzyEquals(num1, num2);
}
exports.fuzzyLessThanOrEquals = fuzzyLessThanOrEquals;
/** Whether `num1` > `num2`, within `epsilon`. */
function fuzzyGreaterThan(num1, num2) {
    return num1 > num2 && !fuzzyEquals(num1, num2);
}
exports.fuzzyGreaterThan = fuzzyGreaterThan;
/** Whether `num1` >= `num2`, within `epsilon`. */
function fuzzyGreaterThanOrEquals(num1, num2) {
    return num1 > num2 || fuzzyEquals(num1, num2);
}
exports.fuzzyGreaterThanOrEquals = fuzzyGreaterThanOrEquals;
/** Whether `num` `fuzzyEquals` an integer. */
function fuzzyIsInt(num) {
    return !isFinite(num) || isNaN(num)
        ? false
        : // Check against 0.5 rather than 0.0 so that we catch numbers that are
            // both very slightly above an integer, and very slightly below.
            fuzzyEquals(Math.abs(num - 0.5) % 1, 0.5);
}
exports.fuzzyIsInt = fuzzyIsInt;
/**
 * If `num` `fuzzyIsInt`, returns it as an integer. Otherwise, returns `null`.
 */
function fuzzyAsInt(num) {
    return fuzzyIsInt(num) ? Math.round(num) : null;
}
exports.fuzzyAsInt = fuzzyAsInt;
/**
 * Rounds `num` to the nearest integer.
 *
 * If `num` `fuzzyEquals` `x.5`, rounds away from zero.
 */
function fuzzyRound(num) {
    if (num > 0) {
        return fuzzyLessThan(num % 1, 0.5) ? Math.floor(num) : Math.ceil(num);
    }
    else {
        return fuzzyGreaterThan(num % 1, -0.5) ? Math.ceil(num) : Math.floor(num);
    }
}
exports.fuzzyRound = fuzzyRound;
/**
 * Returns `num` if it's within `min` and `max`, or `null` if it's not.
 *
 * If `num` `fuzzyEquals` `min` or `max`, it gets clamped to that value.
 */
function fuzzyInRange(num, min, max) {
    if (fuzzyEquals(num, min))
        return min;
    if (fuzzyEquals(num, max))
        return max;
    if (num > min && num < max)
        return num;
    return null;
}
exports.fuzzyInRange = fuzzyInRange;
/**
 * Returns `num` if it's within `min` and `max`. Otherwise, throws an error.
 *
 * If `num` `fuzzyEquals` `min` or `max`, it gets clamped to that value.
 *
 * If `name` is provided, it is used as the parameter name for error reporting.
 */
function fuzzyAssertInRange(num, min, max, name) {
    if (fuzzyEquals(num, min))
        return min;
    if (fuzzyEquals(num, max))
        return max;
    if (num > min && num < max)
        return num;
    throw (0, utils_1.valueError)(`${num} must be between ${min} and ${max}`, name);
}
exports.fuzzyAssertInRange = fuzzyAssertInRange;
/** Returns `dividend % modulus`, but always in the range `[0, modulus)`. */
function positiveMod(dividend, modulus) {
    const result = dividend % modulus;
    return result < 0 ? result + modulus : result;
}
exports.positiveMod = positiveMod;
//# sourceMappingURL=utils.js.map