
defmodule Copi.ThreatModeling do
  @moduledoc """
  Public entry point for threat analysis.
  """

  @doc """
  Analyzes application details using the configured analyzer.
  """
  def analyze(attrs) when is_map(attrs) do
    Copi.ThreatModeling.RuleBasedAnalyzer.analyze(attrs)
  end
end
