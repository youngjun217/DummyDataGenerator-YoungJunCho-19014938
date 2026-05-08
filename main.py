import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(__file__))
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

from generator import generate_and_save, reset_db, DB_PATH


def main() -> None:
    parser = argparse.ArgumentParser(description="주문 더미 데이터 생성기")
    parser.add_argument(
        "-n", "--count",
        type=int,
        default=10,
        help="생성할 주문 수 (기본값: 10)",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="생성 전 DB 초기화",
    )
    args = parser.parse_args()

    print(f"DB 경로: {DB_PATH}")

    if args.reset:
        reset_db()

    print(f"더미 주문 {args.count}건 생성 중...")
    new_orders = generate_and_save(args.count)

    print(f"\n생성 완료: {len(new_orders)}건")
    print(f"{'ID':<10} {'고객명':<15} {'상태':<12} {'총액':>12}  {'생성일'}")
    print("-" * 65)
    for o in new_orders:
        print(
            f"{o['id']:<10} {o['customer_name']:<15} "
            f"{o['status']:<12} {o['total_price']:>12,.0f}원  "
            f"{o['created_at'][:19]}"
        )
    print(f"\norders.json 에 저장되었습니다.")


if __name__ == "__main__":
    main()
