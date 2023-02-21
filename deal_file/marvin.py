import os

DIR = 'videos'

def get_clean_fn(fn:str)->str:
    fn, ext = os.path.splitext(fn)
    return fn

def parse_file_name(fn:str)->str:
    fn = get_clean_fn(fn=fn)
    fn_forward, fn_post = fn.split("_")
    id = int(fn_post)
    return (fn_forward, id)

def run():
    for dir, _, fns in os.walk(DIR):
        fns_parsed = []
        for fn in fns:
            fns_parsed.append(parse_file_name(fn))
        fns_parsed = sorted(fns_parsed, key=lambda x:x[0])
        print(fns_parsed)

if __name__ == "__main__":
    run()