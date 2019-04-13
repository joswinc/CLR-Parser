from prettytable import PrettyTable as pt


def printfirst():
    non_term = []
    term = []
    prod = {}

    def first_set():
        firsts = {}
        row = []

        def first_r(firsts, n_term):
            if n_term in firsts:
                return None

            rules = prod[n_term]
            firsts[n_term] = []

            for p in rules:
                elems = p.split()
                for i in elems:
                    first_r(firsts,i)
                    firsts[n_term].extend(firsts[i])
                    if i in term or 'epsilon' not in prod[i]:
                        break

        for t in term:
            firsts[t] = [t]

        for n_term in non_term:
            if n_term not in firsts:
                first_r(firsts,n_term)

        for i in firsts:
            firsts[i] = list(set(firsts[i]))

        return firsts

    def follow_calc(first):
        follows = {}

        def follow_r(n_term,follows):
            follows[n_term] = []

            if n_term == 'S':
                follows[n_term].append('$')

            for lhs in prod:

                for rule in prod[lhs]:

                    rhs = rule.split()
                    l = [i for i, x in enumerate(rhs) if x == n_term]
                    #if there are multiple occurances of sym in a single prod
                    for pos in l:
                        if pos == len(rhs) - 1:
                            if lhs not in follows.keys():
                                follow_r(lhs,follows)

                            follows[n_term].extend(follows[lhs])
                        else:
                            s = rhs[pos + 1]
                            # print(s)
                            if s not in non_term:
                                f = list(s.split())
                            else:
                                f = first[s]

                            if 'epsilon' in f:
                                f.remove('epsilon')
                                follows[n_term].extend(f)
                                if lhs not in follows.keys():
                                    follow_r(lhs)
                                follows[n_term].extend(follows[lhs])
                            else:
                                follows[n_term].extend(f)

            follows[n_term] = list(set(follows[n_term]))

        for n_term in non_term:
            follow_r(n_term,follows)

        return follows

    def get_grammar():
        fp = open("grammar.txt","r")
        for line in fp:
            line = line.split(" -> ")

            n_term = line[0]
            if n_term not in non_term:
                non_term.append(n_term)

            p = str(line[1]).strip()



            if n_term in prod:
                prod[n_term].append(p)
            else:
                prod[n_term] = [p]

            p = p.split()


            for t in p:
                if t not in non_term:
                    if t not in term:
                        term.append(t)

            for i in non_term:
                if i in term:
                    term.remove(i)

    get_grammar()
    #print(non_term,term,prod)

    first = first_set()


    follows = follow_calc(first)
    print("\n\n")
    #this function returns the first-set of the given rhs (s) of the production
    def first_of_string(s):
        ele = s.split()

        f = []

        for i in ele:
            f.extend(first[i])
            if i not in non_term or "epsilon" not in prod[i]:
                break

        return f


    #printing the table
    a = pt(['Alpha','First set'])
    for x in non_term:
        row = []
        row.append(x)
        row.append(" | ".join(first[x]))
        a.add_row(row)
    print("First:")
    print(a)

    a = pt(['Non-Terminal','Follow set'])
    for x in follows:
        row=[]
        row.append(x)
        row.append(" | ".join(follows[x]))
        a.add_row(row)

    print("\n\nFollow")
    print(a)
    return
