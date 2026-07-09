defmodule Copi.Repo.Migrations.PopulateEopCardUrls do
  use Ecto.Migration

  import Copi.CardMigration


  def change do
    update_card_urls(Path.join(:code.priv_dir(:copi), "/repo/cornucopia/eop-cards-5.0-en.yaml"))
    update_card_urls(Path.join(:code.priv_dir(:copi), "/repo/cornucopia/eop-cards-5.1-en.yaml"))
  end
end
