
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftOPERADOR_CONCATleftOPERADOR_ARITMETICOleftOPERADOR_LOGICOALEATORIO ATRIBUICAO COLCHETES_DIR COLCHETES_ESQ DOIS_PONTOS ENTRADA ESCREVER FIM FUNCAO IDENTIFICADOR INTERPOLATED_STRING NUMERO OPERADOR_ARITMETICO OPERADOR_CONCAT OPERADOR_LOGICO PARENTESES_DIR PARENTESES_ESQ PONTO_E_VIRGULA STRING VIRGULAprogram : statement_liststatement_list : statement\n                      | statement_list statementstatement : FUNCAO IDENTIFICADOR PARENTESES_ESQ parameters PARENTESES_DIR VIRGULA DOIS_PONTOS expression PONTO_E_VIRGULAstatement : FUNCAO IDENTIFICADOR PARENTESES_ESQ parameters PARENTESES_DIR DOIS_PONTOS statement_list FIMoptional_statement_list : statement_list\n                               | emptyempty :parameters : parameters VIRGULA IDENTIFICADORparameters : IDENTIFICADORparameters : expression : IDENTIFICADOR PARENTESES_ESQ arguments PARENTESES_DIRarguments : arguments VIRGULA expressionarguments : expressionarguments : statement : expression PONTO_E_VIRGULAstatements : statementstatement : ESCREVER PARENTESES_ESQ expression PARENTESES_DIR PONTO_E_VIRGULAstatement : IDENTIFICADOR ATRIBUICAO expression PONTO_E_VIRGULAexpression : expression OPERADOR_ARITMETICO expressionexpression : expression OPERADOR_CONCAT expressionexpression : PARENTESES_ESQ expression PARENTESES_DIRexpression : NUMEROexpression : IDENTIFICADORexpression : STRINGexpression : INTERPOLATED_STRINGexpression : ENTRADA PARENTESES_ESQ PARENTESES_DIRexpression : ALEATORIO PARENTESES_ESQ expression PARENTESES_DIR'
    
_lr_action_items = {'FUNCAO':([0,2,3,14,20,38,46,48,51,53,54,],[4,4,-2,-3,-16,-19,-18,4,4,-5,-4,]),'ESCREVER':([0,2,3,14,20,38,46,48,51,53,54,],[8,8,-2,-3,-16,-19,-18,8,8,-5,-4,]),'IDENTIFICADOR':([0,2,3,4,6,14,16,17,20,21,22,23,25,26,38,40,44,46,48,50,51,53,54,],[5,5,-2,15,19,-3,19,19,-16,19,19,19,19,36,-19,19,49,-18,5,19,5,-5,-4,]),'PARENTESES_ESQ':([0,2,3,5,6,8,12,13,14,15,16,17,19,20,21,22,23,25,38,40,46,48,50,51,53,54,],[6,6,-2,17,6,23,24,25,-3,26,6,6,17,-16,6,6,6,6,-19,6,-18,6,6,6,-5,-4,]),'NUMERO':([0,2,3,6,14,16,17,20,21,22,23,25,38,40,46,48,50,51,53,54,],[9,9,-2,9,-3,9,9,-16,9,9,9,9,-19,9,-18,9,9,9,-5,-4,]),'STRING':([0,2,3,6,14,16,17,20,21,22,23,25,38,40,46,48,50,51,53,54,],[10,10,-2,10,-3,10,10,-16,10,10,10,10,-19,10,-18,10,10,10,-5,-4,]),'INTERPOLATED_STRING':([0,2,3,6,14,16,17,20,21,22,23,25,38,40,46,48,50,51,53,54,],[11,11,-2,11,-3,11,11,-16,11,11,11,11,-19,11,-18,11,11,11,-5,-4,]),'ENTRADA':([0,2,3,6,14,16,17,20,21,22,23,25,38,40,46,48,50,51,53,54,],[12,12,-2,12,-3,12,12,-16,12,12,12,12,-19,12,-18,12,12,12,-5,-4,]),'ALEATORIO':([0,2,3,6,14,16,17,20,21,22,23,25,38,40,46,48,50,51,53,54,],[13,13,-2,13,-3,13,13,-16,13,13,13,13,-19,13,-18,13,13,13,-5,-4,]),'$end':([1,2,3,14,20,38,46,53,54,],[0,-1,-2,-3,-16,-19,-18,-5,-4,]),'FIM':([3,14,20,38,46,51,53,54,],[-2,-3,-16,-19,-18,53,-5,-4,]),'ATRIBUICAO':([5,],[16,]),'PONTO_E_VIRGULA':([5,7,9,10,11,19,27,30,31,32,34,39,41,42,52,],[-24,20,-23,-25,-26,-24,38,-22,-20,-21,-27,-12,46,-28,54,]),'OPERADOR_ARITMETICO':([5,7,9,10,11,18,19,27,29,30,31,32,33,34,35,39,42,45,52,],[-24,21,-23,-25,-26,21,-24,21,21,-22,-20,21,21,-27,21,-12,-28,21,21,]),'OPERADOR_CONCAT':([5,7,9,10,11,18,19,27,29,30,31,32,33,34,35,39,42,45,52,],[-24,22,-23,-25,-26,22,-24,22,22,-22,-20,-21,22,-27,22,-12,-28,22,22,]),'PARENTESES_DIR':([9,10,11,17,18,19,24,26,28,29,30,31,32,33,34,35,36,37,39,42,45,49,],[-23,-25,-26,-15,30,-24,34,-11,39,-14,-22,-20,-21,41,-27,42,-10,43,-12,-28,-13,-9,]),'VIRGULA':([9,10,11,17,19,26,28,29,30,31,32,34,36,37,39,42,43,45,49,],[-23,-25,-26,-15,-24,-11,40,-14,-22,-20,-21,-27,-10,44,-12,-28,47,-13,-9,]),'DOIS_PONTOS':([43,47,],[48,50,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'statement_list':([0,48,],[2,51,]),'statement':([0,2,48,51,],[3,14,3,14,]),'expression':([0,2,6,16,17,21,22,23,25,40,48,50,51,],[7,7,18,27,29,31,32,33,35,45,7,52,7,]),'arguments':([17,],[28,]),'parameters':([26,],[37,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> statement_list','program',1,'p_program','main.py',255),
  ('statement_list -> statement','statement_list',1,'p_statement_list','main.py',264),
  ('statement_list -> statement_list statement','statement_list',2,'p_statement_list','main.py',265),
  ('statement -> FUNCAO IDENTIFICADOR PARENTESES_ESQ parameters PARENTESES_DIR VIRGULA DOIS_PONTOS expression PONTO_E_VIRGULA','statement',9,'p_statement_function_inline','main.py',282),
  ('statement -> FUNCAO IDENTIFICADOR PARENTESES_ESQ parameters PARENTESES_DIR DOIS_PONTOS statement_list FIM','statement',8,'p_statement_function_multiline','main.py',290),
  ('optional_statement_list -> statement_list','optional_statement_list',1,'p_optional_statement_list','main.py',294),
  ('optional_statement_list -> empty','optional_statement_list',1,'p_optional_statement_list','main.py',295),
  ('empty -> <empty>','empty',0,'p_empty','main.py',300),
  ('parameters -> parameters VIRGULA IDENTIFICADOR','parameters',3,'p_parameters_multiple','main.py',310),
  ('parameters -> IDENTIFICADOR','parameters',1,'p_parameters_single','main.py',315),
  ('parameters -> <empty>','parameters',0,'p_parameters_empty','main.py',320),
  ('expression -> IDENTIFICADOR PARENTESES_ESQ arguments PARENTESES_DIR','expression',4,'p_expression_function_call','main.py',325),
  ('arguments -> arguments VIRGULA expression','arguments',3,'p_arguments_multiple','main.py',330),
  ('arguments -> expression','arguments',1,'p_arguments_single','main.py',335),
  ('arguments -> <empty>','arguments',0,'p_arguments_empty','main.py',340),
  ('statement -> expression PONTO_E_VIRGULA','statement',2,'p_statement_expression','main.py',348),
  ('statements -> statement','statements',1,'p_statements_single','main.py',353),
  ('statement -> ESCREVER PARENTESES_ESQ expression PARENTESES_DIR PONTO_E_VIRGULA','statement',5,'p_statement_escrever','main.py',358),
  ('statement -> IDENTIFICADOR ATRIBUICAO expression PONTO_E_VIRGULA','statement',4,'p_statement_atribuicao','main.py',363),
  ('expression -> expression OPERADOR_ARITMETICO expression','expression',3,'p_expression_binop','main.py',371),
  ('expression -> expression OPERADOR_CONCAT expression','expression',3,'p_expression_concat','main.py',376),
  ('expression -> PARENTESES_ESQ expression PARENTESES_DIR','expression',3,'p_expression_group','main.py',381),
  ('expression -> NUMERO','expression',1,'p_expression_number','main.py',386),
  ('expression -> IDENTIFICADOR','expression',1,'p_expression_identificador','main.py',391),
  ('expression -> STRING','expression',1,'p_expression_string','main.py',396),
  ('expression -> INTERPOLATED_STRING','expression',1,'p_expression_interpolated_string','main.py',401),
  ('expression -> ENTRADA PARENTESES_ESQ PARENTESES_DIR','expression',3,'p_expression_input','main.py',425),
  ('expression -> ALEATORIO PARENTESES_ESQ expression PARENTESES_DIR','expression',4,'p_expression_random','main.py',430),
]
