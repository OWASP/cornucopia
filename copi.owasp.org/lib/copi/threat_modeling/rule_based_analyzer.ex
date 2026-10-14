
defmodule Copi.ThreatModeling.RuleBasedAnalyzer do
  @moduledoc """
  Performs local, rule-based threat analysis without external services.
  """

  @behaviour Copi.ThreatModeling.Analyzer

  @impl true
  def analyze(attrs) when is_map(attrs) do
    application_type = value(attrs, "application_type")
    authentication = value(attrs, "authentication")
    sensitive_data = value(attrs, "sensitive_data")
    internet_facing = value(attrs, "internet_facing")
    uses_ai = value(attrs, "uses_ai")
    description = value(attrs, "description")

    []
    |> maybe_add(
      authentication == "none",
      "Missing or absent authentication",
      :high,
      "If the application exposes private functionality or data, users may be able to access it without proving their identity.",
      "Identify which endpoints require authentication and enforce authorization on the server."
    )
    |> maybe_add(
      sensitive_data == "yes",
      "Sensitive data exposure",
      :medium,
      "The application may process sensitive information that needs protection.",
      "Classify the data, minimize collection, protect it in transit and at rest, and restrict access."
    )
    |> maybe_add(
      internet_facing == "yes",
      "Public attack surface",
      :medium,
      "An internet-facing application may be exposed to automated attacks and unauthorized requests.",
      "Validate inputs, apply rate limits where appropriate, keep dependencies updated, and monitor security events."
    )
    |> maybe_add(
      uses_ai == "yes",
      "AI-specific security risks",
      :medium,
      "AI-enabled features may introduce prompt injection, unsafe output handling, sensitive-data disclosure, or excessive agency risks.",
      "Treat model output as untrusted input, limit tool permissions, protect sensitive context, and test adversarial prompts."
    )
    |> maybe_add(
      application_type == "api",
      "API access control",
      :medium,
      "APIs can expose data or actions if access controls are incomplete.",
      "Check authorization for every sensitive operation and resource, validate inputs, and avoid exposing unnecessary data."
    )
    |> maybe_add(
      String.trim(description) == "",
      "Insufficient application context",
      :info,
      "The description does not explain the application's components, data flows, or trust boundaries.",
      "Describe the main components, users, external services, sensitive data, and how information moves between them."
    )
    |> add_baseline_observation()
  end

  defp value(attrs, key) do
    attrs
    |> Map.get(key, "")
    |> to_string()
    |> String.trim()
  end

  defp maybe_add(findings, true, title, severity, risk, recommendation) do
    findings ++ [
      %{
        title: title,
        severity: severity,
        risk: risk,
        recommendation: recommendation
      }
    ]
  end

  defp maybe_add(findings, false, _title, _severity, _risk, _recommendation),
    do: findings

  defp add_baseline_observation([]) do
    [
      %{
        title: "Continue validating the design",
        severity: :info,
        risk: "No specific concern was triggered by the current rules. This does not mean the application is secure.",
        recommendation: "Review authentication, authorization, data flows, trust boundaries, logging, error handling, and abuse cases."
      }
    ]
  end

  defp add_baseline_observation(findings), do: findings
end