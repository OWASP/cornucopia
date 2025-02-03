import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper";
import {
  getCardBySuitAndName,
  getCardsFlat,
} from "../../../domain/card/cardController";
import type { PageServerLoad } from "./$types";

export const load = (({ params }) => {
  return {
    card: getCardBySuitAndName(params.suit, params.card),
    cards: getCardsFlat(),
    ASVSRoutes: FileSystemHelper.ASVSRouteMap(),
  };
}) satisfies PageServerLoad;
