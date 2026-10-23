"""Explicit unit boundaries and measurement chains for track modulus b356."""
U('''
軌道模數定義 | 反力是每單位長度的力，位移採同一位置；假定線性均勻支承~Reaction is force per unit length and displacement is collocated; support is linear and uniform | 模型鋼軌分布反力、載點及鄰點撓度~distributed model-rail reaction and deflections at and beside the load
扣件間距換算 | 離散彈簧剛度相同且等距；連續化只適用較長空間尺度~Discrete springs are equally stiff and spaced; homogenization applies only at longer spatial scales | 每個模型支承力位移、間距及鋼軌連續撓度~individual model-support force-displacement, spacing and continuous rail deflection
梁支承特徵參數 | 均勻無限歐拉梁置於線性溫克勒基礎；不含剪切變形~Uniform infinite Euler beam on a linear Winkler foundation; shear deformation is excluded | 模型梁彎曲剛度、支承模數及荷載兩側撓度衰減~model-beam bending rigidity, support modulus and deflection decay on both sides of the load
影響長度量級 | 參數為均勻梁基礎模型的正特徵值；倒數不是反力的硬截止距離~Parameter is a positive characteristic value of a uniform beam-foundation model; its inverse is not a hard reaction cutoff | 跨越數個特徵長度的模型位移與反力剖面~model displacement and reaction profiles extending over several characteristic lengths
無限梁載點撓度 | 單一靜態集中力作用於均勻無限線性梁基礎；遠離端部~One static point load on a uniform infinite linear beam-foundation system, far from ends | 模型荷重元、載點位移及對稱鄰點撓度~model load cell, load-point displacement and symmetric neighboring deflections
載點彎矩估算 | 單一集中力與均勻無限梁基礎；未加入鄰近輪載疊加~One point load and uniform infinite beam foundation; neighboring wheel-load superposition is excluded | 模型鋼軌多位置應變、截面模數及載點座標~model rail strains at multiple positions, section modulus and load coordinate
軸重輪重分配 | 輸入公噸為質量且左右輪靜態均分；不含曲線或動載轉移~Input tonnes represent mass and wheels share static load equally; curve and dynamic load transfer are excluded | 合成車軸質量、左右輪荷重元及水平幾何~synthetic axle mass, left-right wheel load cells and level geometry
動載放大量級 | 放大係數是獨立給定的假設且僅對此靜載；不是通用設計係數~Amplification is an independently assumed factor for this static load, not a universal design factor | 同工況靜動輪重時間序列、速度及輪軌不平順~matched static-dynamic wheel-load histories, speed and wheel-track irregularity
支承區間增量剛度 | 兩點有限差分給出區間增量剛度；只有極小區間才近似切線~A finite difference between two points gives interval incremental stiffness; it approximates a tangent only over a very small interval | 多級模型力位移曲線、端點區間及加密取樣~multilevel model force-displacement curve, endpoint interval and denser sampling
模數空間變異 | 最大、最小及平均模數使用同一載重與測點集合；不是標準差~Maximum, minimum and mean moduli use one load and point set; this is not a standard deviation | 等間距模數剖面、原始力位移及分段統計~equally spaced modulus profile, raw force-displacement and segment statistics
''')
