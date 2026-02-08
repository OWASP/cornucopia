defmodule CopiWeb.ErrorJSONTest do
  use ExUnit.Case, async: true

  test "renders 404" do
    assert CopiWeb.ErrorJSON.render("404.json", %{}) == %{errors: %{detail: "Not Found"}}
  end

  test "renders 500" do
    assert CopiWeb.ErrorJSON.render("500.json", %{}) == %{errors: %{detail: "Internal Server Error"}}
  end

  test "renders 401" do
    assert CopiWeb.ErrorJSON.render("401.json", %{}) == %{errors: %{detail: "Unauthorized"}}
  end

  test "renders 403" do
    assert CopiWeb.ErrorJSON.render("403.json", %{}) == %{errors: %{detail: "Forbidden"}}
  end

  test "renders 422" do
    assert CopiWeb.ErrorJSON.render("422.json", %{}) == %{errors: %{detail: "Unprocessable Entity"}}
  end

  test "renders any other status" do
    result = CopiWeb.ErrorJSON.render("418.json", %{})
    assert is_map(result)
    assert Map.has_key?(result, :errors)
  end
end
