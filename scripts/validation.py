import numpy
import sys
import os
import itertools
import sh
import operator

from sklearn.base import BaseEstimator
from sklearn import svm
from sklearn.naive_bayes import BernoulliNB
from sklearn.feature_extraction import DictVectorizer
from sklearn import cross_validation

from db import get_features_from_rows, get_classes, load_features

def create_weights(features):
  print features

def compute_score(schemes,classes,rows,ml,wp):
  """Computes the score for the features currently in the database using cross-validation"""
  
  if ml == "bnb":
    clf = BernoulliNB()
  elif ml == "svc":
    clf = svm.SVC(kernel="linear")

  features, v = get_features_from_rows(schemes,rows,wp)
  result = cross_validation.cross_val_score(clf, features, classes, cv=5)
  return result

def prepare(depth):
  print "Running extractFeatures for all schemes at depth %i" % depth
  extractFeatures = sh.Command("./scripts/extractFeatures")
  completeArgs = "./data/lib.tiplib %i fa fs la ls ala afa afs als" % depth
  os.system("./scripts/extractFeatures ./data/lib.tiplib %i fa fs la ls ala afa afs als" % depth)
  # extractFeatures(completeArgs)
  # ./data/lib.tiplib 5 fa fs la ls ala afa afs als

def process_combination(args,i,n,classes,rows,depth,ml,wp):
  # remove ""
  args = [arg for arg in args if arg <> ""]
  # If no feature extraction schemes, abort
  if len(args) < 1:
    return False
  # Compute how good it was
  scores = compute_score(args,classes,rows,ml,wp)
  return {"args": args, "mean": scores.mean(), "deviation": scores.std()*2, "depth": depth, "engine": ml, "wp":wp }

def do_step(r,j,n,arg_combinations,mls,wps):
  print "Depth %i" % r 
  prepare(r)
  classes = get_classes() # once per depth is sufficient

  featureRows = load_features()
  results = []
  for ml in mls:
    for wp in wps:
      print "Doing %s with %i,%i,%i,%i" % (ml,wp[0],wp[1],wp[2],wp[3])
      results = results + [process_combination(args,i + j*len(arg_combinations),n,classes,featureRows,r,ml,wp) for i,args in enumerate(arg_combinations)]
  
  return results

def main():
  # Loop over all possible feature extraction schemes
  # TODO: any point with depth=0?

  all_schemes = "fa fs la ls ala afa afs als"
  scheme_combos = ["","fa"], ["","fs"], ["","la"], ["", "ls"], ["","ala"], ["","afa"], ["","afs"], ["","als"]
  mls = ["bnb","svc"]
  weight_combos = [1], [1], [1], [1]
  weight_permutations = list(itertools.product(*weight_combos))
  depth_range = range(2,3)
  arg_combinations = list(itertools.product(*scheme_combos))
  n = len(weight_permutations)*len(mls)*len(depth_range)*len(arg_combinations)
  results = []

  print "Processing %i extraction scheme combinations" % n
    
  for j,r in enumerate(depth_range):
    results = results + do_step(r,j,n,arg_combinations,mls,weight_permutations)
  
  #print results

  # results = [process_combination(arg_combinations[100],1,2), process_combination(arg_combinations[10],2,2)]
  results = [result for result in results if result <> False] # remove False values
  results_sorted = sorted(results, key=operator.itemgetter("mean"))
  #print ""
  print "Index\tAverage score\t\tFeature extraction arguments"
  for i,result in enumerate(results_sorted):
    nice_str = "%i.\t%0.2f (+/- %0.2f)\t\td = %i\t\t%s\t\t%i,%i,%i,%i\t\t" % (i, result['mean'], result['deviation'], result['depth'], result['engine'], result['wp'][0], result['wp'][1], result['wp'][2], result['wp'][3])
    print nice_str, result['args']

if __name__ == '__main__':
  main()
