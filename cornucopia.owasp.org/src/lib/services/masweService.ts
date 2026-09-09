import { MobileMappingService, type MobileMappingData } from './mobileMappingService';

export class MasweService {
    private static readonly service = new MobileMappingService('maswe');

    public static getMasweData(edition: string, version: string): MobileMappingData {
        return this.service.getData(edition, version);
    }

    public static clear(): void {
        this.service.clear();
    }
}
