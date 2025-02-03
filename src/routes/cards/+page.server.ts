import { getSuits } from '../../domain/suit/suitController';
 
export const load = (({ params }) => {
  return {
    suits : getSuits()
  };
});