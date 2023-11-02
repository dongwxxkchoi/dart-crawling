from get_executives import crawl_one_2_many
import get_dart_info 
import argparse
import time
import asyncio
import os

async def main(api, csv_filename, start_year, start_quarter, end_year, end_quarter):

    if api in ['임원목록', '최대주주현황', '타법인출자현황']:
        for year in range(int(start_year), int(end_year) + 1):
            start_q = int(start_quarter) if year == start_year else 1
            end_q = int(end_quarter) if year == end_year and start_year < end_year else 4

            for quarter in range(start_q, end_q + 1):
                await crawl_one_2_many(api, csv_filename, str(year), str(quarter))
                print(f"{api}-{year}-{quarter} finished")
                    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--api', type=str, help='임원목록, 최대주주현황, 타법인출자현황')
    parser.add_argument('--csv_filename', type=str, help='상장사 목록 csv')
    parser.add_argument('--start_year', type=str, help='년도')
    parser.add_argument('--start_quarter', type=str, help='분기(1,2,3,4)')
    parser.add_argument('--end_year', type=str, help='년도')
    parser.add_argument('--end_quarter', type=str, help='분기(1,2,3,4)')

    args = parser.parse_args()

    if args.start_year > args.end_year:
        raise Exception("start year must be earlier than the end year")

    a = time.time()
    asyncio.run(main(args.api, args.csv_filename, args.start_year, args.start_quarter, args.end_year, args.end_quarter))
    print(f"takes {time.time() - a}")

