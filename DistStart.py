

if __name__ == "__main__":
    import sys
    import os
    ndLibrarySupport_dir = os.path.dirname(os.path.abspath(__file__))
    dist_root = os.path.dirname(ndLibrarySupport_dir)
    sys.path.append(dist_root)
    import ndLibrarySupport
    lib_path=dist_root
    if len(sys.argv) >= 2:
        dist_rel=os.path.join(dist_root,sys.argv[1])
        nd_rel=os.path.join(ndLibrarySupport_dir,sys.argv[1])
        if os.path.isdir(sys.argv[1]):
            lib_path=sys.argv[1]
        elif os.path.isdir(dist_rel):    
            lib_path=dist_rel
        elif os.path.isdir(nd_rel):
            lib_path=nd_rel
    if len(sys.argv) >= 3:
        ndman=ndLibrarySupport.manager(lib_path,sys.argv[2])
    else:
        ndman=ndLibrarySupport.manager(lib_path)
