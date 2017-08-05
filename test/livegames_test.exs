defmodule LivegamesTest do
  use ExUnit.Case
  
  setup do
      Application.put_env(:live_games, :web_client, LivegamesTest.TestWebClient)
  end

  test "lists games with ports" do
      games = Livegames.list()
      ports = games
      |> Enum.map( &(&1.port) )
      assert Enum.member?(ports, 9001)
  end

  test "lists empty games" do
      games = Livegames.list_empty()
      assert Enum.count(games) == 107
  end

  test "games have a map name" do
      sierpinski_games = Livegames.list()
      |> Enum.filter( &(&1.map_name == "Sierpinski-triangle.json") )
      assert Enum.count(sierpinski_games) == 20
  end

  test "games have the map itself" do
      a_circle_game = Livegames.list()
      |> Enum.find( &( &1.map_name == "circle.json" ) )
      assert a_circle_game.map_json ==
        File.read!(Path.expand("data/circle.json", __DIR__))
  end
end

defmodule LivegamesTest.TestWebClient do
    @behaviour Livegames.WebClient
    def get!("http://punter.inf.ed.ac.uk/status.html") do
        contents = File.read!(Path.expand("data/game_list_example.html", __DIR__))
        %HTTPoison.Response{
            body: contents
        }
    end
    def get!("http://punter.inf.ed.ac.uk/maps/circle.json") do
        contents = File.read!(Path.expand("data/circle.json", __DIR__))
        %HTTPoison.Response{
            body: contents
        }
    end
    def get!(_) do
        %HTTPoison.Response{
            body: "test data"
        }
    end
 end