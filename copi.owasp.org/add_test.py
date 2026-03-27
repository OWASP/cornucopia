content = open('test/copi_web/live/player_live_test.exs', 'r').read()

# We only replace the LAST end/end which closes describe "Show" and the module
# This is the safest approach - only touch the very end of the file
old_ending = '''      assert render(show_live) =~ player.name
    end
  end
end'''

new_ending = '''      assert render(show_live) =~ player.name
    end

    test "rejects voting on card from different game", %{conn: conn, player: player} do
      {:ok, other_game} = Cornucopia.create_game(%{name: "other game"})
      {:ok, other_player} = Cornucopia.create_player(%{name: "Other", game_id: other_game.id})
      {:ok, game} = Cornucopia.Game.find(player.game_id)
      Copi.Repo.update!(Ecto.Changeset.change(game, started_at: DateTime.truncate(DateTime.utc_now(), :second)))
      {:ok, card} = Cornucopia.create_card(%{category: "C", value: "V2", description: "D", edition: "webapp", version: "2.2", external_id: "EXT3", language: "en", misc: "misc", owasp_scp: [], owasp_devguide: [], owasp_asvs: [], owasp_appsensor: [], capec: [], safecode: [], owasp_mastg: [], owasp_masvs: []})
      {:ok, dealt} = Copi.Repo.insert(%Copi.Cornucopia.DealtCard{player_id: other_player.id, card_id: card.id, played_in_round: 1})
      {:ok, show_live, _html} = live(conn, "/games/#{player.game_id}/players/#{player.id}")
      refute Copi.Repo.get_by(Copi.Cornucopia.Vote, dealt_card_id: dealt.id, player_id: player.id)
    end
  end
end'''

# Safety check - make sure old_ending appears exactly once
count = content.count(old_ending)
if count == 1:
    new_content = content.replace(old_ending, new_ending)
    open('test/copi_web/live/player_live_test.exs', 'w').write(new_content)
    print('Done! Test added successfully.')
elif count == 0:
    print('ERROR: Could not find the target location. File not changed.')
else:
    print(f'ERROR: Found {count} matches - ambiguous. File not changed.')
