"use strict";
// Copyright 2020 Google Inc. Use of this source code is governed by an
// MIT-style license that can be found in the LICENSE file or at
// https://opensource.org/licenses/MIT.
Object.defineProperty(exports, "__esModule", { value: true });
exports.compileStringAsync = exports.compileAsync = exports.compileString = exports.compile = exports.NodePackageImporter = void 0;
const async_1 = require("./compiler/async");
const sync_1 = require("./compiler/sync");
var importer_registry_1 = require("./importer-registry");
Object.defineProperty(exports, "NodePackageImporter", { enumerable: true, get: function () { return importer_registry_1.NodePackageImporter; } });
function compile(path, options) {
    const compiler = (0, sync_1.initCompiler)();
    try {
        return compiler.compile(path, options);
    }
    finally {
        compiler.dispose();
    }
}
exports.compile = compile;
function compileString(source, options) {
    const compiler = (0, sync_1.initCompiler)();
    try {
        return compiler.compileString(source, options);
    }
    finally {
        compiler.dispose();
    }
}
exports.compileString = compileString;
async function compileAsync(path, options) {
    const compiler = await (0, async_1.initAsyncCompiler)();
    try {
        return await compiler.compileAsync(path, options);
    }
    finally {
        await compiler.dispose();
    }
}
exports.compileAsync = compileAsync;
async function compileStringAsync(source, options) {
    const compiler = await (0, async_1.initAsyncCompiler)();
    try {
        return await compiler.compileStringAsync(source, options);
    }
    finally {
        await compiler.dispose();
    }
}
exports.compileStringAsync = compileStringAsync;
//# sourceMappingURL=compile.js.map