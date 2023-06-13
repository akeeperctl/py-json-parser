def main():
    a_biology_team = int(input())
    b_informatic_team = int(input())
    d = 2

    while d % a_biology_team == 0 and d % b_informatic_team == 0:
        d += 1
        print(d % a_biology_team, d % b_informatic_team)
    print(d)


if __name__ == "__main__":
    main()
