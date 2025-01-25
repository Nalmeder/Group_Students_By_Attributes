<h2> Group Students By Sets, Characteristics, or Attributes. </h2>
For creating groups

<br><br>
This was a goof project, copletely utilitarian, so I didn't worry about optimizations in the code.

<h2> Set Up </h2>

Divide students into several 'sets', and create a csv that the main file will read from. For this example, my sets were 'Leader', 'Organizer', and 'Creative.' The students name and set will be saved as an instance of a student class.

<h2> The Algorithm </h2>

In order, the program will
- Assign one student of each set to a group. 1 Leader, 1 Organizer, 1 Creative.
- In most situations, there will be an uneven amount of each. If there are far too many in one set, the program will replace a student of another set in a random group. This process repeats until valid groups can be made from the overflow students.
- If there are less than 3 students overflowing, they are assigned randomly to existing groups, giving groups of size 4 rather than 3.


<h2> Running The Program </h2>
In the commandline

```python3 groups_students.py``` 

Be sure to have a csv in the same directory.





