defmodule MineRoutes do

    def start(mines, edge_map, max_length) do
        mines = [2,3,4]
        edge_map = %{
            0 => [7, 1],
            1 => [2, 7, 3, 0],
            2 => [1, 3],
            3 => [5, 1, 2, 4],
            4 => [5, 3],
            5 => [7, 3, 4, 6],
            6 => [7, 5],
            7 => [0, 1, 5, 6]
        }
        # represents to maximum number of turns in any game
        max_length = 5
        # edge_map = %{
        #     0 => [1],
        #     1 => [2, 0],
        #     2 => [1 ]
        # }
        all_trees = build_trees(mines, edge_map, max_length)
        trees_with_mine_bookends = all_trees
        |> Enum.reduce([], fn(item, a) -> money_trees(item, mines, a) end)
        Enum.count(trees_with_mine_bookends)
        mine_route_map = trees_with_mine_bookends
        |> trees_mapped_by_length
        %{
            "all_trees" => all_trees,
            "trees_with_mine_bookends" => trees_with_mine_bookends,
            "mine_route_map" => mine_route_map
        }
    end

    def build_trees(mines, edge_map, max_length) do
        acc = []
        lists = mines
        |> Enum.map(fn(mine) -> build_tree(acc, mine, edge_map, mines, max_length) end)
        |> flatten_me([])
        |> Enum.uniq
    end

    def money_trees(tree = [head | tail], mines, acc) do
        case head in mines do
            true -> [tree | acc]
            false -> acc
        end
    end

    def add_tree_length_map(tree_length, tree, acc) do
        case Map.has_key?(acc, tree_length) do
            true ->  Map.put(acc, tree_length, [tree | Map.get(acc, tree_length)])
            false -> Map.put(acc, tree_length, tree)
        end
    end

    def trees_mapped_by_length(trees) do
        trees
        |> Enum.reduce(%{}, fn(tree, a) -> add_tree_length_map(Enum.count(tree), tree, a) end)
    end

    def flatten_me(lol = [head | tail], acc) when is_list(head)  do
        lol
        |> Enum.reduce(acc, fn(item, a) -> flatten_me(item, a) end)
    end
    def flatten_me(terminal_list, acc) do
        [terminal_list| acc]
    end


    # acc is a list of sites in the path
    def check_for_subtrees(acc, site, edge_map, mines, max_length) do
        case site in mines && Enum.count(acc) != 1 do
            false -> edge_map
                |> Map.get(site)
                |> Enum.map(fn(next_site) -> build_tree(acc, next_site, edge_map, mines, max_length) end)
            true -> acc
        end
    end
    def build_tree([], mine, edge_map, mines, max_length) do
        [mine] |> check_for_subtrees(mine, edge_map, mines, max_length)
    end
    def build_tree(acc, site, edge_map, mines, max_length) do
        case site in acc || Enum.count(acc) > max_length do
            false -> [site | acc] |> check_for_subtrees(site, edge_map, mines, max_length)
            true -> acc
        end
    end

end


