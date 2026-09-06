"""
mso_graph.py
图/图像网格上的MSO(Monadic Second‑Order Logic)约束
面向CV图像分割：网格图顶点子集（像素掩码）的MSO高层建模
支持：连通子集、禁止孤立点、种子点约束；输出MSO规约；翻译成MIP约束
"""
from typing import List, Dict, Tuple, Set

class MSOGridGraphBuilder:
    """
    网格图MSO建模：每个顶点代表一个像素
    vertex_id: 像素编号 0,1,2,...,N‑1
    edges: 邻接边列表 (u,v)，四邻接
    """
    def __init__(self, height:int, width:int):
        self.H = height
        self.W = width
        self.num_vertex = height * width
        # 像素坐标转顶点id
        self.coord2vid: Dict[Tuple[int,int],int] = {}
        self.vid2coord: Dict[int,Tuple[int,int]] = {}
        vid = 0
        for y in range(height):
            for x in range(width):
                self.coord2vid[(y,x)] = vid
                self.vid2coord[vid] = (y,x)
                vid +=1
        # 构建四邻接边
        self.edges:Set[Tuple[int,int]] = set()
        for y in range(height):
            for x in range(width):
                v = self.coord2vid[(y,x)]
                # 右
                if x+1 < width:
                    nv = self.coord2vid[(y, x+1)]
                    self.edges.add((v,nv))
                # 下
                if y+1 < height:
                    nv = self.coord2vid[(y+1, x)]
                    self.edges.add((v,nv))
        self.edges = list(self.edges)

        # MSO规约文本输出
        self._mso_spec:List[str] = []

    def mso_connected_subset(self, subset_name:str="S"):
        r"""
        MSO：子集 S 必须是连通集合（图论MSO经典公式）
        ∀ T ⊆ S: (T≠∅ ∧ T≠S) → ∃ u∈T, v∈S\T, (u,v)∈E
        """
        spec = f"MSO‑CONNECTED({subset_name}): ∀ T⊆{subset_name}, (T≠∅ ∧ T≠{subset_name}) → ∃u∈T,∃v∈({subset_name}\\T), edge(u,v)"
        self._mso_spec.append(spec)

    def mso_no_isolated_vertex(self, subset_name:str="S"):
        """
        MSO：S中不允许孤立顶点；每个u∈S，至少一个邻居也属于S
        ∀ u∈S: ∃ v∈S, edge(u,v)
        """
        spec = f"MSO‑NO_ISOLATED({subset_name}): ∀u∈{subset_name}: ∃v∈{subset_name}, edge(u,v)"
        self._mso_spec.append(spec)

    def mso_seed_must_in_subset(self, seed_vid_list:List[int], subset_name:str="S"):
        """MSO：种子顶点必须属于子集S（分割种子点）"""
        for sv in seed_vid_list:
            spec = f"MSO‑SEED: vertex({sv}) ∈ {subset_name}"
            self._mso_spec.append(spec)

    def get_mso_spec(self) -> List[str]:
        return self._mso_spec.copy()

    def clear_spec(self):
        self._mso_spec.clear()

    # ========== MSO → MIP 编译函数 ==========
    def translate_no_isolated_to_mip(self, mb, var_map:Dict[int, object]):
        """
        MSO禁止孤立点翻译成MIP约束
        对每个顶点u∈S：sum_{v∈neigh(u)} x_v >= x_u
        x_u=1（像素选中），则至少一个邻居也必须选中
        """
        # 预计算每个顶点邻居
        neigh:Dict[int,List[int]] = {i:[] for i in range(self.num_vertex)}
        for u,v in self.edges:
            neigh[u].append(v)
            neigh[v].append(u)

        for u in range(self.num_vertex):
            xu = var_map[u]
            neighbor_vars = [var_map[v] for v in neigh[u]]
            if len(neighbor_vars) > 0:
                mb.cons(sum(neighbor_vars) >= xu, name=f"no_isolate_u{u}")

    def translate_seed_to_mip(self, mb, var_map:Dict[int, object], seed_vid_list:List[int]):
        """种子点强制属于S：x_seed =1"""
        for sv in seed_vid_list:
            mb.cons(var_map[sv] == 1, name=f"seed_{sv}")


