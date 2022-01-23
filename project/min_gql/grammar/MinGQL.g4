grammar MinGQL;

prog : (EOL? WS? stmt SEMI EOL?)+ EOF;

stmt : PRINT LP expr RP
     | var ASSIGN expr
     ;

expr : LP expr RP
     | lambda_gql
     | map_gql
     | filter_gql
     | var
     | val
     | NOT expr
     | expr KLEENE
     | expr IN expr
     | expr AND expr
     | expr DOT expr
     | expr OR expr
     ;

graph_gql : load_graph
      | set_start
      | cfg
      | set_final
      | add_start
      | add_final
      | LP graph_gql RP
      ;

load_graph : LOAD_GRAPH LP (path | string) RP;
set_start : SET_START LP (graph_gql | var) COMMA (vertices | var) RP ;
set_final : SET_FINAL LP (graph_gql | var) COMMA (vertices | var) RP ;
add_start : ADD_START LP (graph_gql | var) COMMA (vertices | var) RP ;
add_final : ADD_FINAL LP (graph_gql | var) COMMA (vertices | var) RP ;

cfg : CFG ;

vertices : vertex
       | range_gql
       | vertices_set
       | get_reachable
       | get_final
       | get_start
       | get_vertices
       | LP vertices RP
       ;

range_gql : LCB INT DOT DOT INT RCB ;

vertex : INT ;

edges : edge
      | edges_set
      | get_edges
      ;

edge : LP vertex COMMA label COMMA vertex RP
     | LP vertex COMMA vertex RP
     ;

labels : label
       | labels_set
       | get_labels
       ;

label : string ;


lambda_gql : FUN variables COLON expr
           | LP lambda_gql RP ;

map_gql : MAP LP lambda_gql COMMA expr RP;
filter_gql : FILTER LP lambda_gql COMMA expr RP;

get_edges : GET_EDGES LP (graph_gql | var) RP ;
get_labels : GET_LABELS LP (graph_gql | var) RP ;
get_reachable : GET_REACHABLE LP (graph_gql | var) RP;
get_final : GET_FINAL LP (graph_gql | var) RP;
get_start : GET_START LP (graph_gql | var) RP;
get_vertices : GET_VERTICES LP (graph_gql | var) RP;

string : STRING ;
path : PATH ;

vertices_set : LCB (INT COMMA)* (INT)? RCB
             | range_gql ;

labels_set : LCB (STRING COMMA)* (STRING)? RCB ;

edges_set : LCB (edge COMMA)* (edge)? RCB ;

var : IDENT ;

var_edge : LP var COMMA var RP
         | LP var COMMA var COMMA var RP
         | LP LP var COMMA var RP COMMA var COMMA LP var COMMA var RP RP
         ;

variables : lambda_var (COMMA lambda_var)* COMMA?;

lambda_var : var | var_edge ;

val : boolean
    | graph_gql
    | edges
    | labels
    | vertices
    ;

boolean : TRUE | FALSE ;

// TOKENS
COLON : WS? ':' WS? ;
FUN : WS? 'fun' WS? ;
LOAD_GRAPH : WS? 'load_graph' WS? ;
SET_START : WS? 'set_start' WS? ;
SET_FINAL : WS? 'set_final' WS? ;
ADD_START : WS? 'add_start' WS? ;
ADD_FINAL : WS? 'add_final' WS? ;
GET_EDGES: WS? 'get_edges' WS? ;
GET_LABELS: WS? 'get_labels' WS? ;
GET_REACHABLE: WS? 'get_reachable' WS? ;
GET_FINAL: WS? 'get_final' WS? ;
GET_START: WS? 'get_start' WS? ;
GET_VERTICES: WS? 'get_vertices' WS? ;
FILTER : WS? 'filter' WS? ;
MAP : WS? 'map' WS? ;
PRINT : WS? 'print' WS?;

TRUE : WS? 'true' WS?;
FALSE : WS? 'false' WS?;

ASSIGN : WS? '=' WS? ;
AND : WS? '&' WS?;
OR : WS? '|' WS? ;
NOT : WS? 'not' WS? ;
IN : WS? 'in' WS?;
KLEENE : WS? '*' WS?;
DOT : WS? '.' WS? ;
COMMA : WS? ',' WS?;
SEMI : ';' WS?;
LCB : '{' WS?;
RCB : WS? '}' WS?;
LP : '(' WS?;
RP : WS? ')' ;
TRIPLE_QUOT : '"""' ;
ARROW : '->' ;

CFG : TRIPLE_QUOT (CHAR | DIGIT | ' ' | '\n' | ARROW)* TRIPLE_QUOT ;

INT : NONZERO DIGIT* ;

NONZERO : [1-9] ;
DIGIT : [0-9] ;

IDENT : INITIAL_LETTER LETTER* ;
INITIAL_LETTER : '_' | CHAR ;
LETTER : INITIAL_LETTER | DIGIT ;

CHAR : [a-z] | [A-Z] ;
STRING : '"' (CHAR | DIGIT | '_' | ' ')* '"' ;
PATH : '"' (CHAR | DIGIT | '_' | ' ' | '/' | DOT)* '"' ;

WS : [ \t\r]+ -> skip ;
EOL : [\n]+ ;
