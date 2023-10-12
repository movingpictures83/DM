#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# #### Load the example dataset

# In[2]:
import PyIO
import PyPluMA

class DMPlugin:
 def input(self, inputfile):
  self.parameters = PyIO.readParameters(inputfile)

  data_dir = PyPluMA.prefix()+"/"+self.parameters["data_dir"]#inputfile
  self.df = pd.read_table(data_dir, sep="\t")

 def run(self):
  pass

 def output(self, outputfile):
  # #### Start Java VM

  # In[3]:


  from pycausal.pycausal import pycausal as pc
  pc = pc()
  pc.start_vm()


  # #### Load causal algorithms from the py-causal library and Run DM Continuous

  # In[4]:


  from pycausal import search as s
  inputs = self.parameters["inputs"].split(',')#[0,1,2,3]
  outputs = self.parameters["outputs"].split(',')#[4]
  useGES = bool(self.parameters["useGES"])#True
  trueInputs = self.parameters["trueInputs"].split(',')#[0,1,2,3]
  alphaPC = float(self.parameters["alphaPC"])#.05
  verbose = bool(self.parameters["verbose"])#True
  # if useGES == False
  # alphaSober = .05 
  # if useGES == True
  gesDiscount = int(self.parameters["gesDiscount"])#10
  minDiscount = int(self.parameters["minDiscount"])#4
  dm = s.dm(self.df, inputs, outputs, trueInputs, useGES, alphaPC, verbose, gesDiscount, minDiscount)


  # #### DM Continuous' Result's Nodes

  # In[5]:


  dm.getNodes()


  # #### DM Continuous' Result's Edges

  # In[6]:


  dm.getEdges()


  # #### Plot The Result's Graph

  # In[7]:


  import pydot
  #from IPython.display import SVG
  dot_str = pc.tetradGraphToDot(dm.getTetradGraph())
  graphs = pydot.graph_from_dot_data(dot_str)
  graphs[0].write_png(outputfile)
  #svg_str = graphs[0].create_svg()
  #SVG(svg_str)


  # #### Stop Java VM

  # In[8]:


  pc.stop_vm()


  # In[ ]:




