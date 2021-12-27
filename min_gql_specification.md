### Абстрактный синтаксис
```
prog = (EOL? WS? stmt ';' EOL?)+ EOF;

stmt =
    bind of var * expr
  | print of expr

val =
    String of string
  | Int of int
  | Bool of bool
  | Graph of graph
  | Labels of labels
  | Vertices of vertices
  | Edges of edges

expr =
    Var of var                   // переменные
  | Val of val                   // константы
  | Set_start of Set<val> * expr // задать множество стартовых состояний
  | Set_final of Set<val> * expr // задать множество финальных состояний
  | Add_start of Set<val> * expr // добавить состояния в множество стартовых
  | Add_final of Set<val> * expr // добавить состояния в множество финальных
  | Get_start of expr            // получить множество стартовых состояний
  | Get_final of expr            // получить множество финальных состояний
  | Get_reachable of expr        // получить все пары достижимых вершин
  | Get_vertices of expr         // получить все вершины
  | Get_edges of expr            // получить все рёбра
  | Get_labels of expr           // получить все метки
  | Map of lambda * expr         // классический map
  | Filter of lambda * expr      // классический filter
  | Load of path                 // загрузка графа
  | Intersect of expr * expr     // пересечение языков
  | Concat of expr * expr        // конкатенация языков
  | Union of expr * expr         // объединение языков
  | Star of expr                 // замыкание языков (звезда Клини)

lambda = Lambda of variables * expr
```
### Конкретный синтаксис
```
prog -> (stmt ; [EOL])+
stmt -> 'print' '(' expr ')'
      | var = expr
expr -> ( expr )
      | lambda_gql
      | map_gql
      | filter_gql
      | var
      | val
      | 'not' expr
      | expr 'in' expr
      | expr '&' expr
      | expr '.' expr
      | expr '|' expr
      | expr '*'

graph_gql -> load_graph
       | string
       | set_start
       | set_final
       | add_start
       | add_final
       | ( graph_gql )

load_graph -> 'load_graph' '(' (path | string) ')'
set_start -> 'set_start' '(' (graph_gql | var) ',' (vertices | var) ')'
set_final -> 'set_final' '(' (graph_gql | var) ',' (vertices | var) ')'
add_start -> 'add_start' '(' (graph_gql | var) ',' (vertices | var) ')'
add_final -> 'add_start' '(' (graph_gql | var) ',' (vertices | var) ')'

vertices -> vertex
          | range_gql
          | vertices_set
          | get_reachable
          | get_final
          | get_start
          | get_vertices
          | '(' vertices ')'

range -> '{' INT '.' '.' INT '}'

vertex -> INT

edges -> edge
       | edges_set
       | get_edges

edge -> '(' vertex ',' label ',' vertex ')'
      | '(' vertex ',' vertex ')'

labels -> label
        | labels_set
        | get_labels

label -> STRING
path -> PATH

lambda_gql -> 'fun' variables ':' expr
        | 'fun' ':' expr
        | '(' lambda_gql ')'

map_gql -> 'map' '(' lambda_gql ',' expr ')'
filter_gql -> 'filter' '(' lambda_gql ',' expr ')'

variables -> (lambda_var ',')* lambda_var?

var_edge -> '(' var ',' var ')'
          | '(' var ',' var ',' var ')'
          | '(' '(' var ',' var ')' ',' var ',' '(' var ',' var ')' ')'

lambda_var -> var | var_edge ;

get_edges -> 'get_edges' '(' (graph_gql | var) ')'
get_labels -> 'get_labels' '(' (graph_gql | var) ')'
get_reachable -> 'get_reachable' '(' (graph_gql | var) ')'
get_final -> 'get_final' '(' (graph_gql | var) ')'
get_start -> 'get_start' '(' (graph_gql | var) ')'
get_vertices -> 'get_vertices' '(' (graph_gql | var) ')'

vertices_set -> SET<vertex>
             | range_gql
labels_set -> SET<label>
edges_set -> SET<edge>

var -> IDENT

val -> boolean
     | graph_gql
     | edges
     | labels
     | vertices

boolean -> 'true'
         | 'false'

SET<X> -> '{' (X ',')* X? '}'

NONZERO -> [1-9]
DIGIT -> [0-9]
INT -> NONZERO DIGIT*

IDENT -> INITIAL_LETTER LETTER*
INITIAL_LETTER -> '_' | CHAR
LETTER -> INITIAL_LETTER | DIGIT

CHAR -> [a-z] | [A-Z]
STRING -> '"' (CHAR | DIGIT | '_' | ' ')* '"'
PATH: '"' (CHAR | DIGIT | '_' | ' ' | '/' | DOT)* '"'

WS -> [' '\t\r]+
EOL -> [\n]+
```
### Пример 1
Получение множества общих меток графов "wine" и "pizza".
Предварительно в графе "wine" устанавливаются стартовые вершины от 1 до 100.
```
g = load_graph("wine");
new_g = set_start(g, {1..100});
g_labels = get_labels(new_g);
common_labels = g_labels & (load_graph("pizza"));

print(common_labels);
```
### Пример 2
Граф g есть граф "sample", у которого все вершины помечены как финальные, а вершины от 1 до 100 как стартовые.

q1, q2 — запросы, заданные в форме регулярных выражений;

inter — граф, полученный в результате пересечения графа g с регулярным запросом q1;

result — после применения map на множестве ребёр графа inter, остается множество вершин исходного графа g. Последующий фильтр оставляет в этом множестве только стартовые вершины графа g. Данное множество сохраняется в переменной result.
```
tmp = load_graph("sample");
g = set_start(set_final(tmp, get_vertices(tmp)), {1..100});
l1 = "l1" | "l2";
q1 = ("l3" | l1)*;
q2 = "l1" . "l5";
inter = g & q1;
start = get_start(g);
result = filter((fun v: v in start), map((fun ((u_g,u_q1),l,(v_g,v_q1)): u_g), get_edges(inter)));
```