from collections import defaultdict
import sys

class RailwayNetwork:
    def __init__(self):
        # 路線図を格納する辞書
        # 形式: {出発駅: [(到着駅, 距離), ...]}
        self.graph = defaultdict(list)
        # 最長経路の距離
        self.max_distance = 0
        # 最長経路の駅順序
        self.best_path = []

    def add_route(self, start, end, distance):
        """路線を追加するメソッド"""
        self.graph[start].append((end, distance))

    def read_routes(self):
        """標準入力から路線データを読み込む"""
        print("路線データを入力してください（終了はCtrl+D(Mac/Linux) または Ctrl+Z(Windows)）:")
        try:
            for line in sys.stdin:
                # 空行をスキップ
                if not line.strip():
                    continue
                
                # カンマで分割して空白を削除
                parts = [p.strip() for p in line.split(',')]
                
                # 数値に変換
                start = int(parts[0])
                end = int(parts[1])
                distance = float(parts[2])
                
                # 路線を追加
                self.add_route(start, end, distance)
        except (ValueError, IndexError) as e:
            print(f"入力エラー: {e}")
            sys.exit(1)

    def find_longest_path(self):
        """最長経路を見つける"""
        # すべての駅のリストを作成
        all_stations = set(self.graph.keys())
        for routes in self.graph.values():
            for end, _ in routes:
                all_stations.add(end)

        # 各駅を始点として探索
        for start in all_stations:
            # 訪問済みの駅を記録
            visited = {start}
            # 現在の経路を記録
            current_path = [start]
            # 深さ優先探索を開始
            self._dfs(start, visited, current_path, 0)

    def _dfs(self, current, visited, current_path, total_distance):
        # より長い経路が見つかった場合、更新
        if total_distance > self.max_distance:
            self.max_distance = total_distance
            self.best_path = current_path.copy()

        # 現在の駅から行けるすべての駅を探索
        for next_station, distance in self.graph[current]:
            # まだ訪れていない駅の場合
            if next_station not in visited:
                # 訪問済みに追加
                visited.add(next_station)
                # 経路に追加
                current_path.append(next_station)
                
                # 次の駅を探索
                self._dfs(next_station, visited, current_path, 
                        total_distance + distance)
                
                # 探索が終わったら、駅を除去（バックトラック）
                current_path.pop()
                visited.remove(next_station)

    def print_result(self):
        print("\n最長経路:")
        for station in self.best_path:
            # Windows形式の改行コードを使用
            sys.stdout.write(f"{station}\r\n")
        sys.stdout.flush()
        print(f"\n総距離: {self.max_distance}km")

def main():
    # ネットワークのインスタンスを作成
    network = RailwayNetwork()
    
    # 路線データを読み込む
    network.read_routes()
    
    # 最長経路を探索
    network.find_longest_path()
    
    # 結果を出力
    network.print_result()

if __name__ == "__main__":
    main()