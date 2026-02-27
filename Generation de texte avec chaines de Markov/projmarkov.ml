type ltable = (string * string list) list
module STable = Map.Make(String)
module PTable = Map.Make(struct
    type t = string list
    let compare = compare
  end)
type distribution =
  { total : int ;
    amounts : (string * int) list }
type stable = distribution STable.t
type ptable =
  { prefix_length : int ;
    table : distribution PTable.t }


let words str =
  let len = String.length str in
  let rec cree_mot i courant =
    if i >= len then
      match courant with
      | "" -> ["STOP"]
      | mot -> mot :: ["STOP"]
    else
      let c = str.[i] in
      if (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') then
        let mot = courant ^ (String.make 1 c) in
        cree_mot (i + 1) mot
      else
        match courant with
        | "" -> cree_mot (i + 1) ""
        | mot -> mot :: cree_mot (i + 1) ""
  in
  "START" :: cree_mot 0 ""
  
    
let build_ltable words =
  (*let w = "START" :: words @ ["STOP"] in*)
  let rec loop word =
    match word with
    | [] -> []
    | [stop] -> []
    | mot :: succ :: xs -> ajout_assoc mot succ (loop (succ :: xs))
  and ajout_assoc mot succ ltable =
    match ltable with
    | [] -> [ (mot, [succ]) ]
    | (k, lst) :: xs when k = mot -> (k, succ :: lst) :: xs
    | (k, lst) :: xs -> (k, lst) :: ajout_assoc mot succ xs
  in
  loop words
               

let next_in_ltable table word =
  let lst = List.assoc word table in
  let i = Random.int (List.length lst) in
  List.nth lst i

let walk_ltable table =
  let first = next_in_ltable table "START" in
  let rec loop courant acc =
    if courant = "STOP" then List.rev acc
    else let next = next_in_ltable table courant in
      loop next (courant :: acc) 
  in loop first []
  

(* -- Part B -------------------------------------------------------------- *)

(*Ajoutée*)
let rec occur l e =
  match l with
  | [] -> 0
  | x :: xs -> if x = e then 1 + occur xs e
      else occur xs e

let rec remove_all l e =
  match l with
  | [] -> []
  | x :: xs -> if x = e then remove_all xs e 
      else x :: remove_all xs e

let rec compute_distribution l =
  let lst = List.sort String.compare l in
  let tot = List.length l in
  match lst with
  | [] -> { total = 0; amounts = [] }
  | x :: xs ->
      let occ = 1 + occur xs x in
      let new_lst = remove_all xs x in
      let rest = compute_distribution new_lst in
      { total = tot; amounts = (x, occ) :: rest.amounts }
  
  

let rec construire_table_succ words table = 
  match words with 
  |[] -> table 
  |[last] -> table
  |mot :: succ :: xs -> 
      let tab_res = ajouter_succ mot succ table in 
      construire_table_succ (succ :: xs) tab_res

and ajouter_succ mot succ table =
  if STable.mem mot table then 
    let lst = STable.find mot table in 
    STable.add mot (succ::lst) table
  else 
    STable.add mot [succ] table
  
  
      (*let build_htable words =*)
let build_stable words =
  (*let new_words = "START" :: words @ ["STOP"] in*)
  let table_succ = construire_table_succ words STable.empty  in
  STable.map compute_distribution table_succ
    

    (*let next_in_htable table word =*)
let next_in_stable table word = 
  if not( STable.mem word table ) 
  then invalid_arg ("Mot introuvable")
  else
    let {total; amounts} = STable.find word table in
    let r = Random.int total in 
    let rec succ_random amounts r = 
      match amounts with
      |[] -> invalid_arg "impossible de trouver un succ"
      |(succ, freq) :: xs -> if r < freq then succ
          else succ_random xs (r - freq)
    in
    succ_random amounts r
  
    
        (*let walk_htable table =*)
let walk_stable table =
  let first = next_in_stable table "START" in
  let rec loop courant acc =
    if courant = "STOP" then List.rev acc
    else
      let next = next_in_stable table courant in
      loop next (next :: acc) 
  in loop first [first]
    
(* -- Part C -------------------------------------------------------------- *)
let is_word c =
  ('a' <= c && c <= 'z') ||
  ('A' <= c && c <= 'Z') ||
  ('0' <= c && c <= '9') ||
  (Char.code c >= 128 && Char.code c <= 255)

let is_punct c =
  match c with
  | ';' | ',' | ':' | '-' | '"' | '\'' | '?' | '!' | '.' -> true
  | _ -> false

let is_terminator c =
  match c with
  | '?' | '!' | '.' -> true
  | _ -> false
  

let sentences str =
  let len = String.length str in
  let rec loop i mot_cour ph_cour acc =
    if i >= len then
      let ph_cour = if mot_cour <> "" then ph_cour @ [mot_cour] else ph_cour in
      if ph_cour = [] then acc
      else acc @ [ph_cour]
    else
      let c = str.[i] in
      if is_word c then
        loop (i + 1) (mot_cour ^ String.make 1 c) ph_cour acc
      else if is_punct c then
        let ph_cour =
          if mot_cour <> "" then ph_cour @ [mot_cour; String.make 1 c]
          else ph_cour @ [String.make 1 c]
        in
        if is_terminator c then
          loop (i + 1) "" [] (acc @ [ph_cour])
        else
          loop (i + 1) "" ph_cour acc
      else
        let ph_cour =
          if mot_cour <> "" then ph_cour @ [mot_cour]
          else ph_cour
        in
        loop (i + 1) "" ph_cour acc
  in
  loop 0 "" [] []
  
  
let rec start pl =
  if pl <= 0 then []
  else "START" :: start (pl -1)
         
         
let shift l x =
  match l with 
  |[] -> [x]
  |a :: xs -> xs @ [x]
  
  
let add_next lst_pref next table = 
  if PTable.mem lst_pref table then
    let lst_suff = PTable.find lst_pref table in
    PTable.add lst_pref (next :: lst_suff) table
  else 
    PTable.add lst_pref [next] table 
  
  
let build_ptable words pl = 
  let start_prefix = start pl in
  let rec loop tab_acc lst_pref words = 
    match words with 
    | [] -> tab_acc 
    | mot :: xs ->
        let tab_acc = add_next lst_pref mot tab_acc in
        let prefix_suiv = shift lst_pref mot in
        loop tab_acc prefix_suiv xs
  in
  let tab_final = loop PTable.empty start_prefix words in
  let tab_distribution = PTable.map compute_distribution tab_final in
  { prefix_length = pl ; table = tab_distribution }


let random_dist (dist : distribution) : string =
  let total_weight = dist.total in
  let r = Random.int total_weight in
  let rec aux i = function
    | [] -> failwith "Empty distribution"
    | (word, w) :: rest ->
        if i < w then word
        else aux (i - w) rest
  in
  aux r dist.amounts

  
let walk_ptable { table ; prefix_length = pl } =
  let rec loop acc pref_cour = 
    if not (PTable.mem pref_cour table) then
      List.rev acc
    else
      let dist = PTable.find pref_cour table in
      let next = random_dist dist in  (* ← ici on tire un mot aléatoire *)
      if next = "STOP" then
        if Random.bool () then
          loop acc (start pl)  (* recommence avec un nouveau paragraphe *)
        else
          List.rev acc          (* fin de génération *)
      else 
        let pref_suiv = shift pref_cour next in
        loop (next :: acc) pref_suiv
  in
  loop [] (start pl)
  
(*let walk_ptable { table ; prefix_length = pl } =
  let rec loop acc pref_cour = 
    let lst_suff = PTable.find pref_cour table in
    let next = 
      let len = List.length lst_suff in 
      List.nth lst_suff (Random.int len)
    in
    if next = "STOP" then
      if Random.bool () = false 
      then List.rev acc
      else loop acc (start pl)
    else 
      let pref_suiv = shift pref_cour next in
      loop (next :: acc) pref_suiv

  in loop [] (start pl)*)
  
let merge_ptables tl =
  match tl with
  | [] -> { prefix_length = 0; table = PTable.empty }
  | tab :: rest ->
      let prefix_len = tab.prefix_length in

      (* Vérifie que tous les ptable ont le même prefix_length *)
      if List.exists (fun t -> t.prefix_length <> prefix_len) rest then
        invalid_arg "Les tailles de préfixes ne sont pas identiques.";

      (* Convertit les tables en string list -> string list list *)
      let tables_as_lists =
        List.map
          (fun pt ->
             PTable.map
               (fun dist -> List.flatten (List.init dist.total (fun _ ->
                   (* transforme la distribution en liste de suffixes *)
                    List.flatten (
                      List.map (fun (s, n) -> List.init n (fun _ -> s)) dist.amounts
                    )
                  )))
               pt.table)
          tl
      in

      (* Fusionne toutes les tables *)
      let merged_raw_table =
        List.fold_left
          (fun acc table ->
             PTable.fold
               (fun key suffixes acc ->
                  let existing = try PTable.find key acc with Not_found -> [] in
                  PTable.add key (suffixes @ existing) acc)
               table acc)
          PTable.empty
          tables_as_lists
      in

      (* Reconvertit en table de distributions *)
      let final_table = PTable.map compute_distribution merged_raw_table in

      { prefix_length = prefix_len; table = final_table }
