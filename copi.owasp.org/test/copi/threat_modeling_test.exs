defmodule Copi.ThreatModelingTest do
  use ExUnit.Case, async: true

  alias Copi.ThreatModeling

  describe "analyze/1" do
    test "reports missing authentication and API access control concerns" do
      attrs = %{
        "application_type" => "api",
        "authentication" => "none",
        "sensitive_data" => "no",
        "internet_facing" => "no",
        "uses_ai" => "no",
        "description" => "An API used by a web application"
      }

      findings = ThreatModeling.analyze(attrs)
      titles = Enum.map(findings, & &1.title)

      assert "Missing or absent authentication" in titles
      assert "API access control" in titles
      assert Enum.all?(findings, fn finding ->
         finding.severity in [:high, :medium, :info]
       end)
    end

    test "reports AI-specific security risks when AI is enabled" do
      attrs = %{
        "application_type" => "web",
        "authentication" => "session",
        "sensitive_data" => "no",
        "internet_facing" => "no",
        "uses_ai" => "yes",
        "description" => "A website with an AI assistant"
      }

      findings = ThreatModeling.analyze(attrs)

      assert Enum.any?(findings, fn finding ->
               finding.title == "AI-specific security risks"
             end)
    end

    test "reports insufficient context for a blank description" do
      attrs = %{
        "application_type" => "web",
        "authentication" => "session",
        "sensitive_data" => "no",
        "internet_facing" => "no",
        "uses_ai" => "no",
        "description" => "   "
      }

      findings = ThreatModeling.analyze(attrs)

      assert Enum.any?(findings, fn finding ->
               finding.title == "Insufficient application context"
             end)
    end

    test "returns a baseline observation when no specific rules match" do
      attrs = %{
        "application_type" => "web",
        "authentication" => "session",
        "sensitive_data" => "no",
        "internet_facing" => "no",
        "uses_ai" => "no",
        "description" => "A basic website with session authentication"
      }

      findings = ThreatModeling.analyze(attrs)

      assert length(findings) == 1
      assert hd(findings).title == "Continue validating the design"
      assert hd(findings).severity == :info
    end
  end
end