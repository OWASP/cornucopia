/**
 * export_idml_to_pdf.jsx — InDesign ExtendScript
 *
 * Batch-exports all EoP bridge IDML templates to PDF for review.
 *
 * Usage (from InDesign's Scripts panel or Script Editor):
 *   1. Open Adobe InDesign (CC 2019 or later).
 *   2. Choose File > Scripts > Script Editor (or open the Scripts panel).
 *   3. Open this file and click Run (or drag it to the Scripts panel).
 *   4. PDFs will be written to the same folder as each .idml file,
 *      with the same base name and a .pdf extension.
 *
 * Alternatively, run via InDesign Server:
 *   indesignserver -script export_idml_to_pdf.jsx
 */

var TEMPLATES_DIR = File($.fileName).parent.parent + "/resources/templates/";

var IDML_FILES = [
    "eop_ver_about_bridge_lang.idml",
    "eop_ver_instructions1_bridge_lang.idml",
    "eop_ver_instructions2_bridge_lang.idml",
    "eop_ver_strategy-cards_bridge_lang.idml",
    "eop_ver_threat-denialofsvc-cards_bridge_lang.idml",
    "eop_ver_threat-elevofpriv-cards_bridge_lang.idml",
    "eop_ver_threat-infodisclosure-cards_bridge_lang.idml",
    "eop_ver_threat-repudation-cards_bridge_lang.idml",
    "eop_ver_threat-spoofing-cards_bridge_lang.idml",
    "eop_ver_threat-tampering-cards_bridge_lang.idml",
    "eop_ver_deck_bridge_lang.idml",
];

function exportToPDF(idmlPath) {
    var idmlFile = File(idmlPath);
    if (!idmlFile.exists) {
        $.writeln("SKIP (not found): " + idmlPath);
        return false;
    }

    var pdfPath = idmlPath.replace(/\.idml$/, ".pdf");
    var pdfFile = File(pdfPath);

    // Open the IDML document
    var doc = app.open(idmlFile, false);  // false = don't show

    try {
        // Configure PDF export preset — use "High Quality Print" or "[Press Quality]"
        var preset;
        try {
            preset = app.pdfExportPresets.itemByName("[Press Quality]");
        } catch (e) {
            preset = app.pdfExportPresets.itemByName("High Quality Print");
        }

        // Export
        doc.exportFile(ExportFormat.PDF_TYPE, pdfFile, false, preset);
        $.writeln("OK: " + pdfFile.fsName);
        return true;
    } catch (err) {
        $.writeln("FAIL: " + idmlPath + " — " + err.message);
        return false;
    } finally {
        doc.close(SaveOptions.NO);
    }
}

// Main
var ok = 0, fail = 0;
for (var i = 0; i < IDML_FILES.length; i++) {
    var result = exportToPDF(TEMPLATES_DIR + IDML_FILES[i]);
    if (result) ok++; else fail++;
}

alert("Export complete: " + ok + " succeeded, " + fail + " failed.\n" +
      "PDFs are in resources/templates/");
