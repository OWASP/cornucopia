defmodule Copi.Cornucopia.Card do
  use Ecto.Schema
  import Ecto.Changeset

  schema "cards" do
    field :capec, {:array, :string}
    field :category, :string
    field :description, :string
    field :edition, :string
    field :external_id, :string
    field :language, :string
    field :misc, :string
    field :owasp_appsensor, {:array, :string}
    field :owasp_asvs, {:array, :string}
    field :owasp_masvs, {:array, :string}
    field :owasp_mastg, {:array, :string}
    field :owasp_scp, {:array, :string}
    field :owasp_devguide, {:array, :string}
    field :safecode, {:array, :string}
    field :value, :string
    field :version, :string
    field :biml, :string
    field :url, :string, default: ""

    timestamps()
  end

  @doc false
  def changeset(card, attrs) do
    card
    |> cast(attrs, [:category, :value, :description, :misc, :edition, :external_id, :language, :version, :owasp_scp, :owasp_devguide, :owasp_asvs, :owasp_appsensor, :capec, :safecode, :owasp_mastg, :owasp_masvs, :biml, :url])
    |> validate_required([:category, :value, :description, :misc, :edition, :external_id, :language, :version, :owasp_scp, :owasp_devguide, :owasp_asvs, :owasp_appsensor, :capec, :safecode, :owasp_mastg, :owasp_masvs])
  end
end
