// export_idml_to_pdf.jsx
// InDesign ExtendScript to batch export IDML templates to PDF for review.

#target indesign

function main() {
    // Check if documents are already open
    if (app.documents.length > 0) {
        alert("Please close all open documents before running this script.");
        return;
    }

    // Set the source folder containing the templates
    var scriptFile = new File($.fileName);
    var rootDir = scriptFile.parent.parent;
    var sourceFolder = new Folder(rootDir + "/resources/templates");
    
    if (!sourceFolder.exists) {
        alert("Could not find the templates folder: " + sourceFolder.fsName);
        return;
    }

    // Set the output folder
    var outFolder = new Folder(rootDir + "/output/pdf_reviews");
    if (!outFolder.exists) {
        outFolder.create();
    }

    // We specifically want to review the newly created bridge layouts
    var filesToProcess = [
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
        "eop_ver_deck_bridge_lang.idml"
    ];

    // Get a PDF export preset (High Quality Print is usually a safe default for review)
    var myPDFExportPreset = app.pdfExportPresets.item("[High Quality Print]");
    if (!myPDFExportPreset.isValid) {
        // Fallback to the first available preset if HQ Print is not found
        myPDFExportPreset = app.pdfExportPresets.item(0);
    }

    app.scriptPreferences.userInteractionLevel = UserInteractionLevels.NEVER_INTERACT;
    var successCount = 0;
    var errors = [];

    for (var i = 0; i < filesToProcess.length; i++) {
        var idmlFile = new File(sourceFolder + "/" + filesToProcess[i]);
        if (!idmlFile.exists) {
            errors.push("File not found: " + filesToProcess[i]);
            continue;
        }

        try {
            // Open the IDML file
            var doc = app.open(idmlFile);
            
            // Generate the output PDF path
            var baseName = filesToProcess[i].replace(/\.idml$/i, "");
            var pdfFile = new File(outFolder + "/" + baseName + ".pdf");
            
            // Export the document to PDF
            doc.exportFile(ExportFormat.PDF_TYPE, pdfFile, false, myPDFExportPreset);
            
            // Close the document without saving changes
            doc.close(SaveOptions.NO);
            
            successCount++;
        } catch (e) {
            errors.push("Error processing " + filesToProcess[i] + ": " + e.message);
            // Ensure doc is closed if it errored during export
            if (app.documents.length > 0) {
                app.activeDocument.close(SaveOptions.NO);
            }
        }
    }
    
    app.scriptPreferences.userInteractionLevel = UserInteractionLevels.INTERACT_WITH_ALL;

    var msg = "Export complete. " + successCount + " files exported to PDF.\nOutput folder: " + outFolder.fsName;
    if (errors.length > 0) {
        msg += "\n\nErrors encountered:\n" + errors.join("\n");
    }
    alert(msg);
}

main();
