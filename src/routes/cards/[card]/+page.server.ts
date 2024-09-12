import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper";
import {
  getCardById,
  getCardsFlat,
} from "../../../domain/card/cardController";
import type { PageServerLoad } from "./$types";

export const load = (({ params }) => {
  return {
    card: getCardById(String(params.card).toUpperCase()),
    cards: getCardsFlat(),
    ASVSRoutes: FileSystemHelper.ASVSRouteMap(),
  };
}) satisfies PageServerLoad;
