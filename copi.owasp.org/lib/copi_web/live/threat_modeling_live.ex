
defmodule CopiWeb.ThreatModelingLive do
  use CopiWeb, :live_view

  @impl true
  def mount(_params, _session, socket) do
    {:ok, assign(socket, :findings, nil)}
  end

  @impl true
  def handle_event("analyze", %{"threat_model" => attrs}, socket) do
    findings = Copi.ThreatModeling.analyze(attrs)
    {:noreply, assign(socket, :findings, findings)}
  end
end
