defmodule Copi.Card do
  use Ecto.Schema
  import Ecto.Changeset

  schema "cards" do
    field :capec, :string
    field :category, :string
    field :description, :string
    field :edition, :string
    field :language, :string
    field :misc, :string
    field :owasp_appsensor, :string
    field :owasp_asvs, :string
    field :owasp_scp, :string
    field :safecode, :string
    field :value, :string
    field :version, :string

    timestamps()
  end

  @doc false
  def changeset(card, attrs) do
    card
    |> cast(attrs, [:category, :value, :description, :misc, :edition, :language, :version, :owasp_scp, :owasp_asvs, :owasp_appsensor, :capec, :safecode])
    |> validate_required([:category, :value, :description, :misc, :edition, :language, :version, :owasp_scp, :owasp_asvs, :owasp_appsensor, :capec, :safecode])
  end
end
