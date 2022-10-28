<center><font face="黑体" size = 8><strong>分布式算法作业</strong></font></center></br>

<center><font face="黑体" size = 5>联系：lightac@mail.ustc.edu.cn		作者：Zezhong</font></center></br>

# <center><font face = 'Times New Roman'>Problem 1</font></center>
<font face=" 黑体" size = 4>安全性（$safety$）板书：</font>
<font face=" 黑体" size = 4>思考：是否对于每一执行的每一断言都成立的断言/性质就是不变式呢？</font>
<font face=" 黑体" size = 4>答：</font></br>
<font face=" 宋体" size = 4>对于每一执行的每一个断言都成立的性质不一定是不变式。因为在这个过程之中可能会有状态无法达到，这样尽管每一次执行的每一个断言都成立，但是它仍然不是不变式。</font></br>
<font face=" 黑体" size = 4>不变式的定义：</font>

<font face=" 宋体" size = 4>断言$P$是$S$的一个不变式，如果$(1)$对所有的$\gamma \in I$，$P(\gamma)$成立，且$(2)$${P}$$\Rightarrow$${P}$</font>
<font face=" 宋体" size = 4>例子，假设一个整数变量$x$。假设$x$初始值为$0$。状态转移方式为：</font>

```C++
	if x == 1 then x = 2
```
<font face=" 宋体" size = 4>设断言：</font>
$$
x < 2
$$
<font face=" 宋体" size = 4>显然，断言如同公式$(1)$所示都成立。但是不变式要求中要求每次转移过程之中保持不变，当$x=1$式断言成立，当经过转移后$x=2$时，断言并不成立。因此，不满足不变式定义中的$(2)$条件。</font></br>

# <center><font face = 'Times New Roman'>Problem 2</font></center>
<font face=" 黑体" size = 4>分布式算法$PPT$ $ch33$: $P9$ $Ex$</font>
<font face=" 黑体" size = 4>证明：图$G$里一结点从$p_r$可达当且仅当它曾设置过自己的$parent$变量。</font>
<font face=" 黑体" size = 4>答：</font></br>

```C++
//算法2.2
//构造生成树（code for pi 0≤i≤n-1）
//初值：parent=nil；集合children和other均为φ
upon receiving no message:
    if i=r and parent=nil then { //根尚未发送M
        send M to all neighbors;
        parent:=i;} //根的双亲置为自己
upon receiving M from neighbor pj
	if parent=nil then {//pi此前未收到过M，M是pi收到的第1个msg
		parent:=j;
		send <parent> to pj; //pj是pi的双亲
		send M to all neighbors except pj;
	}else //pj不可能是pi的双亲，pi收到的M不是第1个msg
 		send<reject> to pj;
upon receiving <parent> from neighbor pj:
	children:=children∪{ j }; //pj是pi的孩子，将j加入孩子集
	if children∪other 包含了除parent外的所有邻居 then terminate;
upon receiving <reject> from neighbor pj:
	other:=other∪{ j }; //将j加入other，通过非树边发送的msg。
	if children∪other包含了除pi的双亲外的所有邻居 then terminate
```
</br>

<font face=" 黑体" size = 4>1.  证明：必要性</font>
<font face=" 宋体" size = 4>图$G$里一结点从$p_r$可达则它曾设置过自己的$parent$变量。由于图$G$是消息传播过程之中不断被生成的，因此任意一个结点在收到$message$之后才会被加入到图中，这样这个结点才会可达。当这个结点收到了$message$，由于是容许执行，程序会执行$8$至$14$行，判断它的$parent$是否为空。如果为空，则为设置自己的$parent$变量。如果不为空，则代表已经设置过了。</font></br>
<font face=" 黑体" size = 4>2.  证明：充分性</font>
<font face=" 宋体" size = 4>图$G$里一结点设置过自己的$parent$变量则该结点从$p_r$可达。首先，$message$是从$p_r$发出的。如果结点设置过自己的$parent$变量则代表程序执行了代码的第$10$行，那么代码的第$8$行程序也执行过了。因此结点收到了$message$，综合$message$是从$p_r$发出的，可以推断出该结点是从$p_r$可达的。</font></br>


# <center><font face = 'Times New Roman'>Problem 3</font></center>
<font face=" 黑体" size = 4>分布式算法$PPT$ $ch33$: $P30$ $Ex2.1$</font>
<font face=" 黑体" size = 4>分析在同步和异步模型下，$convergecast$算法的时间复杂性。</font>
<font face=" 黑体" size = 4>答：</font></br>
<font face=" 黑体" size = 4>$Convergecast$算法：</font>
<font face=" 宋体" size = 4>每个叶子结点$p_i$发送$x_i$至双亲。//启动者</font>
<font face=" 宋体" size = 4>对每个非叶结点$p_j$，设$p_j$有$k$个孩子$p_{i1}, …, p_{ik}$, $p_j$等待$k$个孩子的$msg$ $v_{i1}$, $v_{i2}$, …, $v_{ik}$，当$p_j$收到所有孩子的$msg$之后将$v_j$=$max(x_j, v_{i1}, …, v_{ik})$发送到$p_j$的双亲。</font></br>

<font face=" 黑体" size = 4>1 同步模型：</font>
<font face=" 宋体" size = 4>引理：在汇集算法的每个容许执行里，树中每个高为$t$子树根结点在第$t$轮里收到所有$children$的$message$。</font>
<font face=" 宋体" size = 4>利用数学归纳法：$t=1$时，每个叶子结点在第$1$轮里收到来自于自身的$message$。假设树上每个高为$t-1$的子树根结点在第$t-1$轮收到了$message$。假设$p_i$到叶子结点的距离为$t$，设$p_j$是$p_i$的$children$。因为$p_j$到叶子结点的距离为$t-1$。则$p_j$在$t-1$轮收到$message$。通过算法过程可知，在第$t$轮$p_i$将收到来自于$p_j$的$message$。</font>
<font face=" 宋体" size = 4>汇集是从所有结点收集信息至根。如果这个过程是同步的那么整个汇集过程的轮数为树的高度$d$。因此对于同步模型，存在汇集的时间复杂度为$O(d)$的算法。其中$d$为树的高度。</font></br>

<font face=" 黑体" size = 4>2 异步模型：</font>
<font face=" 宋体" size = 4>引理：在汇集算法的每个容许执行里，树中每个高为$t$子树根结点至多在第$t$轮里收到所有$children$的$message$。</font>
<font face=" 宋体" size = 4>利用数学归纳法：$t=1$时，每个叶子结点至多在第$1$轮里收到来自于自身的$message$。假设树上每个高为$t-1$的子树根结点至多在第$t-1$轮收到了$message$。假设$p_i$到叶子结点的距离为$t$，设$p_j$是$p_i$的$children$。因为$p_j$到叶子结点的距离为$t-1$。则$p_j$至多在$t-1$轮收到$message$。通过算法过程可知，至多在第$t$轮$p_i$将收到来自于$p_j$的$message$。</font>
<font face=" 宋体" size = 4>汇集是从所有结点收集信息至根。如果这个过程是异步的那么整个汇集过程的轮数至多为树的高度$d$。因此对于异步模型，存在汇集的时间复杂度为$O(d)$的算法。其中$d$为树的高度。</font></br>

# <center><font face = 'Times New Roman'>Problem 4</font></center>
<font face=" 黑体" size = 4>分布式算法$PPT$ $ch33$: $P30$ $Ex2.3$</font>
<font face=" 黑体" size = 4>证明$Alg2.3$构造一棵以$P_r$为根的$DFS$树。</font>
<font face=" 黑体" size = 4>答：</font></br>

```c++
//算法2.3 构造DFS生成树，以Pr为根
Code for processor Pi, 0≤i ≤ n-1
var parent: init nil;
children: init φ;
unexplored: init all the neighbors of Pi
//未访问过的邻居集
upon receiving no msg:
	if (i=r) and (parent=nil) then { //当Pi为根且未发送M时
		parent := i; //将parent置为自身的标号
		任意Pj ∈ unexplored;
		将Pj从unexplored中删去; //若Pr是孤立结点,4-6应稍作修改
		send M to Pj;
	}//endif
upon receiving M from neighbor Pj:
	if parent=nil then { //Pi此前未收到M
		parent := j; //Pj是Pi的父亲
		从unexplored中删Pj
		if unexplored ≠φ then {
			任意Pk ∈ unexplored;
			将Pk从unexplored中删去;
			send M to Pk;
		} else send <parent> to parent; //当Pi的邻居均已访问过，返回到父亲
	}else send <reject> to Pj; //当Pi已访问过时
upon receiving <parent> or <reject> from neighbor Pj:
	if received <parent> then add j to children; 
	//Pj是Pi的孩子
	if unexplored = φ then { //Pi的邻居均已访问
		if parent ≠ i then send <parent> to parent; 
		//Pi非根，返回至双亲
		terminate; //以Pi为根的DFS子树已构造好！
	}else { //选择Pi的未访问过的邻居访问之
		Pk ∈ unexplored;
		将Pk从unexplored中删去；
		send M to Pk;
	}
```
</br>

<font face=" 黑体" size = 4>1 连通性：</font>
<font face=" 宋体" size = 4>反证法。若图$G$不连通。则在图$G$中存在相邻结点$P_j$和$P_i$。$P_j$从$P_r$可达但$P_i$从$P_r$不可达。不可达意味着$P_i$的$parent$没有被设置为空且$P_i$不是$P_j$的$children$。但是，$P_j$可达意味着$P_j$的$parent$不为空且$P_i$属于$unexplored$集合之中。算法的$14$至$21$行决定了$P_j$会向$P_i$发送$message$并使得，$P_i$的$parent$设置为$P_j$且$P_i$成为$P_j$的$children$。因此这个过程之中产生矛盾，故图$G$是连通的。</font></br>
<font face=" 黑体" size = 4>2 无环性：</font>
<font face=" 宋体" size = 4>反证法。假设图$G$中存在一个环$P_1, P_2, P_3, ..., P_t, P_1$。不妨设$P_1$为环中最先收到$message$的点。当$P_t$收到消息时，它会将消息传递给$P_1$，此时$P_1$的$parent$已经不为空，所以根据代码第23行。$P_1$将向$P_t$发送一个$reject$消息且不会讲$P_t$设置为$parent$，同时由于$P_t$没有收到$P_1$发送的$parent$消息，因此不会将$P_1$设置成为自己的$children$。由于环的存在$P_1$是从$P_t$可达的。那么，$P_1$应该是$P_t$的$children$。产生矛盾。因此图$G$是无环的。</font></br>
<font face=" 黑体" size = 4>3 $DFS$树：</font>
<font face=" 宋体" size = 4>只需证明在有子结点和兄弟结点没有访问时，子结点总是优先加入树中即可。设存在结点$P_x$，$P_y$与$P_t$直接相连。假设$P_x$为访问的子节点（程序在第$18$到$21$行先访问的），$P_y$为兄弟结点。那么$P_t$只会在$P_x$向$P_t$发送一个$parent$只会才会向$P_y$发送$message$（第$24$行）。又由程序可知$P_x$向所有的相邻结点都发送过$message$之后才会向$P_t$发送$parent$（第$27$至$30$行）。因此，$P_x$的子结点永远优先于$P_y$先收到消息，先加入树$G$。综上，$G$为$DFS$树。</font></br>

# <center><font face = 'Times New Roman'>Problem 5</font></center>
<font face=" 黑体" size = 4>分布式算法$PPT$ $ch33$: $P30$ $Ex2.4$</font>
<font face=" 黑体" size = 4>证明$Alg2.3$的时间复杂性为$O(m)$。</font>
<font face=" 黑体" size = 4>答：</font></br>
<font face=" 黑体" size = 4>消息复杂度：</font>
<font face=" 宋体" size = 4>对于任意一条边来说，可能传递的消息最多有$4$个，即两个$M$其中$2$个相应$M$的消息（$parent$，$reject$），因此消息复杂度为$O(m)$。其中$m$为图的边数。</font></br>
<font face=" 黑体" size = 4>1 同步模型：</font>
<font face=" 宋体" size = 4>在每一轮中，根据算法可知，有且只有一条消息（$M$，$parent$，$reject$）在传递，从代码的第$12$、$21$、$23$、$28$、$34$行发送消息的语句中分析可以发现消息只发送一个结点，除去根节点外，所有的处理器都是在收到消息之后才能被激活，所以，不存在多个处理器在同一轮发消息的情况，因此时间复杂度与消息复杂度一致均为$O(m)$。其中$m$为图的边数。</font></br>
<font face=" 黑体" size = 4>2 异步模型：</font>
<font face=" 宋体" size = 4>对于异步算法分析算法可知，一个时刻内至多一条消息（$M$，$parent$，$reject$）在传递，因此时间复杂度与消息复杂度是一致的。均为$O(m)$。其中$m$为图的边数。</font></br>

# <center><font face = 'Times New Roman'>Problem 6</font></center>
<font face=" 黑体" size = 4>分布式算法$PPT$ $ch33$: $P30$ $Ex2.5$</font>
<font face=" 黑体" size = 4>修改$Alg2.3$获得一新算法，使构造$DFS$树的时间复杂性为$O(n)$，并证明。</font>
<font face=" 黑体" size = 4>答：</font></br>
<font face=" 黑体" size = 4>1 方法一：</font>
<font face=" 宋体" size = 4>可以考虑在每个处理器中维护一本地变量（变量之中存储访问信息），同时添加一消息类型，在处理器$P_i$转发$message$时，发送消息$notice$通知其余的未访问过的邻居，这样其邻居在转发$message$时便不会向$P_i$转发，这样时间复杂度为$O(n)$。其中$n$是图中的点数。</font></br>
<font face=" 黑体" size = 4>2 方法二：</font>
<font face=" 宋体" size = 4>在消息$message$和$parent$信息中维护一发送数组，记录已经转发过$message$的处理器名称，这样可以使得每个处理器被发送一次。</font>
<font face=" 宋体" size = 4>两种方式都是避免向已转发过$message$的处理器发送消息$message$，这样$DFS$树外的边不再耗时，时间复杂度也降为$O(n)$。</font></br>

# <center><font face = 'Times New Roman'>Problem 7</font></center>
<font face=" 黑体" size = 4>分布式算法$PPT$ $ch34$: $P9$ $Ex3.1$</font>
<font face=" 黑体" size = 4>证明同步环系统中不存在匿名的、一致性的领导者选举算法。</font>
<font face=" 黑体" size = 4>答：</font></br>
<font face=" 黑体" size = 4>$Lemma3.1$：</font><font face=" 宋体" size = 4>在环$R$上算法$A$的容许执行里，对于每一轮$k$，所有处理器的状态在第$k$轮结束时是相同的。</font></br>
<font face="黑体" size = 4>证明过程：</font><font face=" 宋体" size = 4>在匿名系统中，每个处理器在系统中具有相同的状态机。设R是大小为$n>1$的环（非均匀），由 $Lemma3.1$ 可知，设算法$ A$ 是使环$R$上某个处理器为 $leader$ 的算法。因为环是同步的，且只有一种初始配置。在每轮里，各处理器均发出同样的$message$，所以在各轮里各个处理器接收到相同的$message$，则状态改变也相同。这也表明$R$上$A$唯一合法执行。所以所有处理器要么同为$leader$，要么同时不为$leader$。故同步环系统中匿名的、一致性的领导者选举算法的算法是不存在的。</font></br>


# <center><font face = 'Times New Roman'>Problem 8</font></center>
<font face=" 黑体" size = 4>分布式算法$PPT$ $ch34$: $P9$ $Ex3.2$</font>
<font face=" 黑体" size = 4>证明异步环系统中不存在匿名的领导者选举算法。</font>
<font face=" 黑体" size = 4>答：</font></br>
<font face="黑体" size = 4>证明过程：</font><font face=" 宋体" size = 4>每个处理器的初始状态和状态机相同，除了接收消息的时间可能不同外，接收到的消息序列也相同。所以最终处理器的状态也是一致的。由于处理器处理一条消息至多需要 $1$ 单位时间，若某时刻某个处理器宣布自己是 $leader$（接收到了$m$条消息），则在有限时间内（$m$个时间单位内），其它处理器也会宣布自己是 $leader$。故异步环系统中匿名的领导者选举算法是不存在的。</font></br>

# <center><font face = 'Times New Roman'>Problem 9</font></center>
<font face=" 黑体" size = 4>分布式算法$PPT$ $ch35$: $P39$ $Ex3.9$</font>
<font face=" 黑体" size = 4>证明：若将环$R^{Rev}_n$划分为长度为$j$($j$是2的方幂)的连续片断，则所有这些片断是次序等价的。</font>
<font face=" 黑体" size = 4>答：</font></br>
<font face=" 黑体" size = 4>序等价定义：</font><font face=" 宋体" size = 4>两个环$x_0, x_1, …, x_{n-1}$和$y_0, y_1,…,y_{n-1}$是(次)序等价的，若对每个$i$和$j$，$x_i \textless x_j$, 当且仅当$y_i \textless y_j$。</font></br>
<font face="黑体" size = 4>证明过程：</font><font face=" 宋体" size = 4>若$j$为片段的长度，不妨设$j=2^k$。假设$m_1$和$m_2$在同一个片段上，$n_1$和$n_2$在同一个片段上，且这个两个片段相邻。显然$m_1$与$m_2$有公式$(2)$和$(3)$的表示方法。</font>
$$
m_1 = \sum_{i=0}^{logj - 1}a_i \times 2^{i}
$$
$$
m_2 = \sum_{i=0}^{logj - 1}b_i \times 2^{i}
$$
<font face=" 宋体" size = 4>$m_1$和$m_2$在同一个片段上，可得：</font>
$$
|m_1 - m_2| < j = 2^k
$$
<font face=" 宋体" size = 4>由公式$(4)$分析可知一定存在$t \in [1, k]$使得$a_t \neq b_t$。反证法，若任意$t \in [0, k]$使得$a_t \neq b_t$，则由于$m_1 \neq m_2$，因此$|m_1 - m_2|  \geq j$。与$m_1$和$m_2$在同一个片段上发生矛盾。取$t_0=min\{t\}$，最小下标经过反转之后得到最大下标，因此：</font>
$$
sign(rev(m_1)-rev(m_2)) = sign(a_{t_0} - b_{t_0})
$$
<font face=" 宋体" size = 4>其中$rev(m)$是$m$的二进制表示的逆序列。同时，</font>
$$
n_1 = m_1 + j = \sum_{i=0}^{logj - 1}a_i \times 2^{i} + 2^k
$$
$$
n_2 = m_2 + j = \sum_{i=0}^{logj - 1}b_i \times 2^{i} + 2^k
$$
<font face=" 宋体" size = 4>由公式$(6)$和$(7)$可知，$m_1$和$n_1$以及$m_2$和$n_2$这两对前$k$位相同。由于$t_0 \in [0, k]$，因此有：</font>
$$
sign(rev(n_1)-rev(n_2)) = sign(a_{t_0} - b_{t_0})
$$
<font face=" 宋体" size = 4>综上，这两个片段是序等价，根据等价关系具有传递性，可知所有的片段都是次序等价的。</font>