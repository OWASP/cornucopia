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
end
