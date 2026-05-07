defmodule CopiWeb.CoreComponentsTest do
  use CopiWeb.ConnCase, async: true
  import Phoenix.LiveViewTest
  import CopiWeb.CoreComponents
  use Phoenix.Component


  test "renders modal" do
    assigns = %{show: true, id: "modal"}
    
    html = rendered_to_string(~H"""
    <.modal id="modal" show>
      Modal Content
    </.modal>
    """)
    
    assert html =~ "Modal Content"
    assert html =~ "id=\"modal\""
  end

  test "renders flash" do
    assigns = %{flash: %{"info" => "Success Message"}}
    
    html = rendered_to_string(~H"""
    <.flash_group flash={@flash} />
    """)
    
    assert html =~ "Success Message"
    assert html =~ "Success!"
  end

  test "renders simple form" do
    assigns = %{form: to_form(%{"name" => "test"}, as: :user)}
    
    html = rendered_to_string(~H"""
    <.simple_form for={@form}>
      <.input field={@form[:name]} label="Name" />
      <:actions>
        <button>Save</button>
      </:actions>
    </.simple_form>
    """)
    
    assert html =~ "Name"
    assert html =~ "value=\"test\""
    assert html =~ "Save"
  end

  test "renders table" do
    assigns = %{rows: [%{id: 1, name: "Test"}]}
    
    html = rendered_to_string(~H"""
    <.table id="users" rows={@rows}>
      <:col :let={user} label="Name"><%= user.name %></:col>
    </.table>
    """)
    
    assert html =~ "Test"
    assert html =~ "Name"
  end
  
  test "renders back link" do
    assigns = %{}
    html = rendered_to_string(~H"""
    <.back navigate="/home">Back</.back>
    """)
    
    assert html =~ "href=\"/home\""
    assert html =~ "Back"
  end
  
  test "renders icon" do
    assigns = %{}
    html = rendered_to_string(~H"""
    <.icon name="hero-home" />
    """)
    
    assert html =~ "hero-home"
  end
  
  test "renders input types" do
    assigns = %{form: to_form(%{"check" => ["Option"]}, as: :user)}
    
    html = rendered_to_string(~H"""
      <.input field={@form[:check]} type="checkbox" label="Check me" options={[{"Option", "true"}]} />
    """)
    assert html =~ "type=\"checkbox\""
    assert html =~ "Option"
  end
  
  test "renders disconnected flash" do
    assigns = %{flash: %{}}
    html = rendered_to_string(~H"""
    <.flash_group flash={@flash} />
    """)
    assert html =~ "client-error"
    assert html =~ "server-error"
  end

  test "renders select and textarea" do
    assigns = %{form: to_form(%{"role" => "admin", "bio" => "text"}, as: :user)}
    html = rendered_to_string(~H"""
      <.input field={@form[:role]} type="select" options={["admin", "user"]} label="Role" />
      <.input field={@form[:bio]} type="textarea" label="Bio" />
    """)
    assert html =~ "Role"
    assert html =~ "admin"
    assert html =~ "Bio"
    assert html =~ "textarea"
  end

  test "renders list" do
    assigns = %{}
    html = rendered_to_string(~H"""
    <.list>
      <:item title="Title">Item 1</:item>
    </.list>
    """)
    assert html =~ "Title"
    assert html =~ "Item 1"
  end

  test "renders card_drop_zone for current player with no card played" do
    import CopiWeb.CoreComponents.TableComponents
    player = %{name: "Alice"}
    assigns = %{}
    html = rendered_to_string(~H"""
    <.card_drop_zone
      player={player}
      player_card={nil}
      is_current_player={true}
      first_card_played={nil}
      highest_scoring_card={nil}
    >
      content
    </.card_drop_zone>
    """)
    assert html =~ "You can play"
  end

  test "renders card_drop_zone for current player with first card played" do
    import CopiWeb.CoreComponents.TableComponents
    player = %{name: "Alice"}
    first_card = %{card: %{category: "Spades"}}
    assigns = %{}
    html = rendered_to_string(~H"""
    <.card_drop_zone
      player={player}
      player_card={nil}
      is_current_player={true}
      first_card_played={first_card}
      highest_scoring_card={nil}
    >
      content
    </.card_drop_zone>
    """)
    assert html =~ "should"
    assert html =~ "Spades"
  end

  test "renders card_drop_zone waiting for other player" do
    import CopiWeb.CoreComponents.TableComponents
    player = %{name: "Bob"}
    assigns = %{}
    html = rendered_to_string(~H"""
    <.card_drop_zone
      player={player}
      player_card={nil}
      is_current_player={false}
      first_card_played={nil}
      highest_scoring_card={nil}
    >
      content
    </.card_drop_zone>
    """)
    assert html =~ "Waiting for Bob"
  end

  test "renders card_drop_zone with played card" do
    import CopiWeb.CoreComponents.TableComponents
    player = %{name: "Alice"}
    player_card = %{id: 1}
    highest = %{id: 1}
    assigns = %{}
    html = rendered_to_string(~H"""
    <.card_drop_zone
      player={player}
      player_card={player_card}
      is_current_player={true}
      first_card_played={nil}
      highest_scoring_card={highest}
    >
      <span>PlayedContent</span>
    </.card_drop_zone>
    """)
    assert html =~ "PlayedContent"
    assert html =~ "ring-amber-300"
  end

  test "renders vote_card when player_card is nil" do
    import CopiWeb.CoreComponents.TableComponents
    game = %{players: []}
    assigns = %{}
    html = rendered_to_string(~H"""
    <.vote_card player_card={nil} game={game} />
    """)
    refute html =~ "hero-hand-thumb-up"
  end

  test "renders vote_card when player_card is set" do
    import CopiWeb.CoreComponents.TableComponents
    player_card = %{votes: []}
    game = %{players: [%{}, %{}]}
    assigns = %{}
    html = rendered_to_string(~H"""
    <.vote_card player_card={player_card} game={game} />
    """)
    assert html =~ "hero-hand-thumb-up"
  end

  test "renders button components" do
    import CopiWeb.CoreComponents.Buttons
    uri = "http://example.com/game/123"
    assigns = %{}
    html = rendered_to_string(~H"""
    <.button type="submit">Click Me</.button>
    <.primary_button disabled={false}>Save</.primary_button>
    <.primary_button disabled={true}>Disabled</.primary_button>
    <.copy_url_button uri={uri} />
    """)
    assert html =~ "Click Me"
    assert html =~ "Save"
    assert html =~ "Disabled"
    assert html =~ "bg-zinc-400"
    assert html =~ "copy-url-container"
    assert html =~ "http://example.com/game/123"
  end

  test "renders header components" do
    import CopiWeb.CoreComponents.Headers
    assigns = %{}
    html = rendered_to_string(~H"""
    <.header class="my-cls">
      Title
      <:subtitle>Sub</:subtitle>
      <:actions>Act</:actions>
    </.header>
    <.header1 id="h1" class="h1-cls">Heading One</.header1>
    <.header2 class="h2-cls">Heading Two</.header2>
    """)
    assert html =~ "Title"
    assert html =~ "Sub"
    assert html =~ "Act"
    assert html =~ "Heading One"
    assert html =~ "Heading Two"
  end

  test "translate_error with count uses plural form" do
    result = CopiWeb.CoreComponents.translate_error({"must be at most %{count} characters", [count: 5, validation: :length]})
    assert is_binary(result)
  end

  test "translate_errors/2 returns error messages for matching field" do
    errors = [{:name, {"can't be blank", [validation: :required]}}]
    assert CopiWeb.CoreComponents.translate_errors(errors, :name) == ["can't be blank"]
    assert CopiWeb.CoreComponents.translate_errors(errors, :email) == []
  end
end
