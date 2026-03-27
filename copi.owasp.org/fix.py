content = open('lib/copi_web/controllers/api_controller.ex', encoding='utf-8').read() 
old = '      player = Enum.find(game.players, fn player - == player_id end)\n      dealt_card = Enum.find(player.dealt_cards, fn dealt_card - == dealt_card_id end)\n      if player && dealt_card do' 
new = '      player = Enum.find(game.players, fn player - == player_id end)\n      if player do\n        dealt_card = Enum.find(player.dealt_cards, fn dealt_card - == dealt_card_id end)\n        if dealt_card do' 
result = content.replace(old, new) 
open('lib/copi_web/controllers/api_controller.ex', 'w', encoding='utf-8').write(result) 
print('DONE' if old not in result else 'FAILED') 
