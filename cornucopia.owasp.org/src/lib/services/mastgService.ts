import { MobileMappingService, type MobileMappingData } from './mobileMappingService';

export class MastgService {
    private static readonly service = new MobileMappingService('mastg');

    public static getMastgData(edition: string, version: string): MobileMappingData {
        return this.service.getData(edition, version);
    }

    public static clear(): void {
        this.service.clear();
    }
}
