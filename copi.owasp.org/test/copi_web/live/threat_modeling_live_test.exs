
defmodule CopiWeb.ThreatModelingLiveTest do
  use CopiWeb.ConnCase

  import Phoenix.LiveViewTest

  test "page displays the threat modeling form", %{conn: conn} do
    {:ok, _view, html} = live(conn, "/threat-modeling")

    assert html =~ "Threat Modeling"
    assert html =~ "Analyze Threats"
  end

  test "submitting the form displays security findings", %{conn: conn} do
    {:ok, view, _html} = live(conn, "/threat-modeling")

    html =
      view
      |> form("#threat-model-form",
        threat_model: %{
          application_type: "api",
          authentication: "none",
          sensitive_data: "yes",
          internet_facing: "yes",
          uses_ai: "yes",
          description: "An internet-facing API that uses an AI service"
        }
      )
      |> render_submit()

    assert html =~ "Potential Threats and Recommendations"
    assert html =~ "Missing or absent authentication"
    assert html =~ "Sensitive data exposure"
    assert html =~ "Public attack surface"
    assert html =~ "AI-specific security risks"
    assert html =~ "API access control"
  end
end
