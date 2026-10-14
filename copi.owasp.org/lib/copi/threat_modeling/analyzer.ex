defmodule Copi.ThreatModeling.Analyzer do
  @moduledoc """
  Defines the interface for threat analysis implementations.
  """

  @callback analyze(map()) :: [map()]
end