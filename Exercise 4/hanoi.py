import sys


def create_domain_file(domain_file_name, n_, m_):
    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    domain_file = open(domain_file_name, 'w')  # use domain_file.write(str) to write to domain_file
    domain_file.write("Propositions:\n")

    for disk in disks:
        for peg in pegs:
            domain_file.write(f"{disk}_on_{peg} ")
            domain_file.write(f"{disk}_not_on_{peg} ")

    domain_file.write("\nActions:\n")
    for i in range(len(disks)):
        for peg1 in pegs:
            for peg2 in pegs:
                if peg1 != peg2:
                    domain_file.write(f"Name: move_{disks[i]}_from_{peg1}_to_{peg2}\n")

                    domain_file.write("Pre: ")
                    for j in range(i - 1, -1, -1):
                        domain_file.write(f"{disks[j]}_not_on_{peg1} {disks[j]}_not_on_{peg2} ")
                    domain_file.write(f"{disks[i]}_on_{peg1} {disks[i]}_not_on_{peg2}\n")

                    domain_file.write(f"Add: {disks[i]}_on_{peg2} {disks[i]}_not_on_{peg1}\n")

                    domain_file.write(f"Delete: {disks[i]}_on_{peg1} {disks[i]}_not_on_{peg2}\n")
    domain_file.close()


def create_problem_file(problem_file_name_, n_, m_):
    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    problem_file = open(problem_file_name_, 'w')  # use problem_file.write(str) to write to problem_file

    problem_file.write("Initial state: ")
    for disk in disks:
        problem_file.write(f"{disk}_on_{pegs[0]} ")
    for disk in disks:
        for peg in pegs[1:]:
            problem_file.write(f"{disk}_not_on_{peg} ")

    problem_file.write("\nGoal state: ")
    for disk in disks:
        problem_file.write(f"{disk}_on_{pegs[m_ - 1]} ")
    for disk in disks:
        for peg in pegs[:m_ - 1]:
            problem_file.write(f"{disk}_not_on_{peg} ")
    problem_file.close()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: hanoi.py n m')
        sys.exit(2)

    n = int(float(sys.argv[1]))  # number of disks
    m = int(float(sys.argv[2]))  # number of pegs

    domain_file_name = 'hanoi_%s_%s_domain.txt' % (n, m)
    problem_file_name = 'hanoi_%s_%s_problem.txt' % (n, m)

    create_domain_file(domain_file_name, n, m)
    create_problem_file(problem_file_name, n, m)
