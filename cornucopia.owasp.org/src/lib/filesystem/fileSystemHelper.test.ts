import {expect, describe, it} from 'vitest';
import { FileSystemHelper } from './fileSystemHelper';
import path from 'path';

describe('FileSystemHelper tests', () => {
    it("should get directories.", async () => {
        const directories = FileSystemHelper.getDirectories(path.normalize(__dirname + '/../../../data/website/pages/cards'));
        expect(directories).toBeDefined();
        expect(directories.length).toBeGreaterThan(0);
        
    });

    it('test has file', () => {
        const hasFile = FileSystemHelper.hasFile(path.normalize(__dirname + '/../../../data/website/pages/cards/en/index.md'));
        expect(hasFile).toBe(true);

        const hasNoFile = FileSystemHelper.hasFile(path.normalize(__dirname + '/../../../data/website/pages/cards/en/nonexistent.md'));
        expect(hasNoFile).toBe(false);
    });

    it('test has dir', () => {
        const hasDir = FileSystemHelper.hasDir(path.normalize(__dirname + '/../../../data/website/pages/cards/en'));
        expect(hasDir).toBe(true);

        const hasNoDir = FileSystemHelper.hasDir(path.normalize(__dirname + '/../../../data/website/pages/nonexistent'));
        expect(hasNoDir).toBe(false);
    });

    it("should get files.", async () => {
        const files = FileSystemHelper.getFiles(path.normalize(__dirname + '/../../../data/news/20231201-development-post'));
        expect(files).toBeDefined();
        expect(files.length).toBe(2);
    });

    it("should read data from a path.", async () => {
        const data = FileSystemHelper.getDataFromPath('data/website/pages/about');
        expect(data).toBeDefined();
        expect(data['en']).toBeDefined;

        const emptyData = FileSystemHelper.getDataFromPath('data/website/pages/nonexistent');
        expect(emptyData).toBeDefined();
        expect(emptyData['en']).toBeUndefined();
    });

    it("should get the ASVSRouteMap files.", async () => {
        const files = FileSystemHelper.ASVSRouteMap();
        expect(files).toBeDefined();
        expect(files.length).toBeGreaterThan(0);
        expect(files[0]['Path']).toBe('/taxonomy/ASVS-4.0.3/01-architecture-design-and-threat-modeling/01-secure-software-development-lifecycle');

        const files2 = FileSystemHelper.ASVSRouteMap('5.0');
        expect(files2).toBeDefined();
        expect(files2.length).toBeGreaterThan(0);
        expect(files2[0]['Path']).toBe('/taxonomy/ASVS-5.0/01-encoding-and-sanitization/01-encoding-and-sanitization-architecture');
    });

    it("should get current page name by route.", async () => {
        const folderName = FileSystemHelper.getCurrentPageNameByRoute('/taxonomy/ASVS-4.0.3/01-architecture-design-and-threat-modeling/01-secure-software-development-lifecycle');
        expect(folderName).toBe('01-secure-software-development-lifecycle');

        const folderNameEmpty = FileSystemHelper.getCurrentPageNameByRoute('');
        expect(folderNameEmpty).toBe('Requirements Mapping');
    });

    it("should get data by route.", async () => {
        const expectedCategories = [
            '01-secure-software-development-lifecycle',
            '02-authentication-architecture',
            '03-session-management-architecture'
        ];

        //Test with a file route
        let [noCategories, fileContent] = FileSystemHelper.getDataByRoute('/taxonomy/ASVS-4.0.3/01-architecture-design-and-threat-modeling/01-secure-software-development-lifecycle', 'en');
        expect(noCategories).toBeDefined();
        expect(fileContent).toBeDefined();
        expect(fileContent.length).toBeGreaterThan(0);
        expect(noCategories.length).toBe(0);

        //Test with a language that does not have a translation, should fallback to English
        let [noLangCategories, engFileContent] = FileSystemHelper.getDataByRoute('/taxonomy/ASVS-4.0.3/01-architecture-design-and-threat-modeling/01-secure-software-development-lifecycle', 'es');
        expect(noLangCategories).toBeDefined();
        expect(engFileContent).toBeDefined();
        expect(engFileContent.length).toBeGreaterThan(0);
        expect(noLangCategories.length).toBe(0);

        //Test with a folder route
        let [categories, content] = FileSystemHelper.getDataByRoute('/taxonomy/ASVS-4.0.3/01-architecture-design-and-threat-modeling', 'en');
        expect(categories).toBeDefined();
        expect(content).toBeDefined();
        expect(content.length).toBe(0);
        expect(categories.length).toBeGreaterThan(0);
        expectedCategories.forEach((category) => {
            expect(categories).toContain(category);
        });

        //Test with the root taxonomy route
        let [categoriesRoot, contentRoot] = FileSystemHelper.getDataByRoute('/taxonomy', 'en');
        expect(categoriesRoot).toBeDefined();
        expect(contentRoot).toBeDefined();
        expect(contentRoot.length).toBe(0);
        expect(categoriesRoot.length).toBeGreaterThan(0);
        const expectedRootCategories = [
            'asvs-5.0',
            'stride',
            'attacks'
        ];
        expectedRootCategories.forEach((category) => {
            expect(categoriesRoot).toContain(category);
        });

        //Test with the root taxonomy route
        let [asvsCategories, asvsRoot] = FileSystemHelper.getDataByRoute('/taxonomy/asvs-4.0.3', 'en');
        expect(asvsCategories).toBeDefined();
        expect(asvsRoot).toBeDefined();
        expect(asvsRoot.length).toBe(0);
        expect(asvsCategories.length).toBeGreaterThan(0);
        const expectedASVSCategories = [
            '01-architecture-design-and-threat-modeling',
            '02-authentication'
        ];
        expectedASVSCategories.forEach((category) => {
            expect(asvsCategories).toContain(category);
        });
    });
});