import fred.orm as fredmodel
from fred.daemon import engine

metadata = fredmodel.Base.metadata

def main():
    metadata.drop_all(bind=engine)
    metadata.create_all(bind=engine)

if __name__ == "__main__":
    main()
