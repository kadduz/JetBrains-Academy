def load_matrix():
    nr, nc = map(int, input("Enter size of matrix: ").split())
    print("Enter matrix:")
    mtx = []
    for y in range(nr):
        row = list(map(float, input().split()))
        if len(row) != nc:
            raise ValueError("Enter the correct values")
        mtx.append(row)
    return mtx


def add_mtx(ma, mb):
    if len(ma) != len(mb) or len(ma[0]) != len(mb[0]):
        print("ERROR")
        return None
    mc = []
    for rowa, rowb in zip(ma, mb):
        mc.append([ela + elb for ela, elb in zip(rowa, rowb)])
    return mc


def scale_mtx(mtx, constant):
    return [[el * constant for el in row] for row in mtx]


def mul_mtx(ma, mb):
    if len(ma[0]) != len(mb):
        print("ERROR")
        return None
    mc = []
    for rowa in ma:
        rowc = []
        for cb in range(len(mb[0])):
            colb = [mb[rb][cb] for rb in range(len(mb))]
            rowc.append(sum(ela * elb for ela, elb in zip(rowa, colb)))
        mc.append(rowc)
    return mc


def transpose_mtx(ma):
    mc = []
    for ca in range(len(ma[0])):
        rowc = [ma[ra][ca] for ra in range(len(ma))]
        mc.append(rowc)
    return mc


def transpose_side_mtx(ma):
    mc = []
    for ca in range(len(ma[0])-1, -1, -1):
        rowc = [ma[ra][ca] for ra in range(len(ma)-1, -1, -1)]
        mc.append(rowc)
    return mc


def transpose_ver_mtx(ma):
    return [rowa[::-1] for rowa in ma]


def transpose_hor_mtx(ma):
    return ma[::-1]


def show_mtx(mtx):
    if mtx:
        print("The result is:")
        for row in mtx:
            print(" ".join(map(str, row)))


def det_mtx(mtx):
    mtxl = len(mtx)
    if len(mtx[0]) != mtxl:
        print("ERROR")
        return None
    elif mtxl == 1:
        return mtx[0][0]
    elif mtxl == 2:
        return mtx[0][0] * mtx[1][1] - mtx[0][1] * mtx[1][0]
    else:
        det = 0
        for i in range(mtxl):
            min_mtx = []
            for row in mtx[1:]:
                min_mtx.append([row[j] for j in range(mtxl) if j != i])
            det += (-1)**i * mtx[0][i] * det_mtx(min_mtx)
        return det


def cof_mtx(mtx):
    mtxlr = len(mtx)
    mtxlc = len(mtx[0])
    if mtxlc != mtxlr:
        print("ERROR")
        return None
    elif mtxlr == 1:
        return [1]
    else:
        c_mtx = []
        for r0 in range(mtxlr):
            c_row = []
            for c0 in range(mtxlc):
                min_mtx = []
                for r1 in range(mtxlr):
                    if r1 != r0:
                        min_mtx_row = []
                        for c1 in range(mtxlc):
                            if c1 != c0:
                                min_mtx_row.append(mtx[r1][c1])
                        min_mtx.append(min_mtx_row)
                c_row.append((-1)**(r0 + c0) * det_mtx(min_mtx))
            c_mtx.append(c_row)
        return c_mtx


while True:
    print("1. Add matrices\n2. Multiply matrix by a constant\n"
          "3. Multiply matrices\n4. Transpose matrix\n"
          "5. Calculate a determinant\n6. Inverse matrix\n0. Exit")
    choice = int(input("Your choice: "))
    if choice == 0:
        break
    elif choice == 1:
        a = load_matrix()
        b = load_matrix()
        c = add_mtx(a, b)
        show_mtx(c)
    elif choice == 2:
        a = load_matrix()
        const = int(input("Enter constant: "))
        c = scale_mtx(a, const)
        show_mtx(c)
    elif choice == 3:
        a = load_matrix()
        b = load_matrix()
        c = mul_mtx(a, b)
        show_mtx(c)
    elif choice == 4:
        print("\n1. Main diagonal\n2. Side diagonal\n"
              "3. Vertical line\n4. Horizontal line")
        choice = int(input("Your choice: "))
        if choice in (1, 2, 3, 4):
            c = []
            a = load_matrix()
            if choice == 1:
                c = transpose_mtx(a)
            elif choice == 2:
                c = transpose_side_mtx(a)
            elif choice == 3:
                c = transpose_ver_mtx(a)
            elif choice == 4:
                c = transpose_hor_mtx(a)
            show_mtx(c)
    elif choice == 5:
        a = load_matrix()
        print(f"The result is:\n{det_mtx(a)}")
    elif choice == 6:
        a = load_matrix()
        determinant = det_mtx(a)
        cfm = cof_mtx(a)
        cfmt = transpose_mtx(cfm)
        c = scale_mtx(cfmt, 1 / determinant)
        show_mtx(c)
