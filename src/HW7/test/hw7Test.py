"""
   Created for HW7
   Baselined: 18 April 2011  
   Modified:  27 April 2011
   @author:   Chulakorn Aritajati
"""

import unittest
import HW7.prod.hw7 as hw

class TestCrcCard(unittest.TestCase):
    
    def test001BugFix(self):
        self.assertRaises(ValueError, hw.CrcCard, "", 2, 42)
            

class TestSizeMethod(unittest.TestCase):
    
    def test001BugFix(self):
        aSizeMatrix = hw.SizeMatrix()
        component1 = hw.Component("compoent1", 10, 100, None)
        component2 = hw.Component("compoent1", 0, 3, None)
        aSizeMatrix.addComponent(component1)
        aSizeMatrix.addComponent(component2)
        self.assertEquals(aSizeMatrix.count(), 2, 'Count is not correct')
        self.assertEquals(aSizeMatrix.validCount(), 1, 'Count is not correct')
        aCrcCardVS = hw.CrcCard("component1", 2, "vS", "")
        aResultVS = aSizeMatrix.estimateSize(aCrcCardVS)
        self.assertEquals(aResultVS.name, "component1", aResultVS.name)
        self.assertEquals(aResultVS.getLocCount(), 20, aResultVS.getLocCount())
        self.assertEquals(aResultVS.getMethodCount(), 2, aResultVS.getMethodCount())
    
    def test002BugFix(self):
        aSizeMatrix = hw.SizeMatrix()
        component1 = hw.Component("compoent1", 10, 100, None)
        component2 = hw.Component("compoent1", 0, 3, None)
        aSizeMatrix.addComponent(component2)
        aSizeMatrix.addComponent(component1)
        self.assertEquals(aSizeMatrix.count(), 2, 'Count is not correct')
        self.assertEquals(aSizeMatrix.validCount(), 1, 'Count is not correct')
        aCrcCardVS = hw.CrcCard("component1", 2, "vS", "")
        aResultVS = aSizeMatrix.estimateSize(aCrcCardVS)
        self.assertEquals(aResultVS.name, "component1", aResultVS.name)
        self.assertEquals(aResultVS.getLocCount(), 20, aResultVS.getLocCount())
        self.assertEquals(aResultVS.getMethodCount(), 2, aResultVS.getMethodCount())
        
class TestComponentIterationMap(unittest.TestCase):
    
        def test001Constructure(self):
            try:
                aIterationMapo = hw.ComponentIterationMap(4)
            except:
                self.fail()
        def test002Constructure(self):
            self.assertRaises(ValueError, hw.ComponentIterationMap, "hi")
            
        def test003Constructure(self):
            self.assertRaises(ValueError, hw.ComponentIterationMap, -1)
            
        def test004AddComponent(self):
            component1 = hw.Component("compoent1", 2, 3, None)
            component2 = hw.Component("compoent1", 2, 3, None)
            aIterationMapo = hw.ComponentIterationMap(4)
            aIterationMapo.addComponent(component2, [0, 1, 2])
            number = aIterationMapo.addComponent(component1, [0, 1, 2])
            self.assertEquals(number, 2, number)
            
        def test005AddComponent(self):
            aIterationMapo = hw.ComponentIterationMap(4)
            self.assertRaises(ValueError, aIterationMapo.addComponent, "hi", [0, 1, 2])
        
        def test006AddComponent(self):
            component1 = hw.Component("compoent1", 2, 3, None)
            aIterationMapo = hw.ComponentIterationMap(4)
            self.assertRaises(ValueError, aIterationMapo.addComponent, component1, [-1, 1, 2])
            
        def test007AddComponent(self):
            component1 = hw.Component("compoent1", 2, 3, None)
            aIterationMapo = hw.ComponentIterationMap(4)
            self.assertRaises(ValueError, aIterationMapo.addComponent, component1, [0, 1, 2, 4, 4])
        
        def test008AddComponent(self):
            component1 = hw.Component("compoent1", 2, 3, None)
            aIterationMapo = hw.ComponentIterationMap(4)
            self.assertRaises(ValueError, aIterationMapo.addComponent, component1, [0, 1, 0])
        
        def test009Iter(self):
            try:
                aIterationMapo = hw.ComponentIterationMap(4)
                aIt = iter(aIterationMapo)
            except:
                self.fail()
        
        def test0012Iter(self):
                aIterationMapo = hw.ComponentIterationMap(4)
                component1 = hw.Component("compoent1", 2, 3, None)
                aIterationMapo.addComponent(component1, [0, 1, 2])
                aIt = iter(aIterationMapo)
                x = aIt.next()
                self.assertEquals(x, ['compoent1', 0, 1, 2], "Wrong")
                
class TestComponentCalendar(unittest.TestCase):
    
        def test001Constructure(self):
            try:
                aCalendar = hw.Calendar()
            except:
                self.fail()
        
        def test002Constructure(self):
            aCalendar = hw.Calendar()
            self.assertRaises(ValueError, aCalendar.addDay, -1)
            
        def test003AddComponent(self):
            aCalendar = hw.Calendar()
            aCalendar.addDay(100)
            aCalendar.addDay(80)
            number = aCalendar.addDay(50)
            self.assertEquals(number, 3, number)
        
        def test004Iter(self):
            try:
                aCalendar = hw.Calendar()
                aCalendar.addDay(80)
                aIt = iter(aCalendar)
            except:
                self.fail()
        
        def test005Iter(self):
            aCalendar = hw.Calendar()
            aCalendar.addDay(80)
            aIt = iter(aCalendar)
            x = aIt.next()
            self.assertEquals(x, 80, "Wrong")

class TestSchedule(unittest.TestCase):
     
    def test001Constructure(self):
            try:
                aIterationMapo = hw.ComponentIterationMap(4)
                component1 = hw.Component("compoent1", 2, 3, None)
                aIterationMapo.addComponent(component1, [0, 1, 2])
                aCalendar = hw.Calendar()
                aCalendar.addDay(80)
                aSchedule = hw.Schedule(aIterationMapo, aCalendar)
            except:
                self.fail()
    def test002Constructure(self):
            aIterationMapo = hw.ComponentIterationMap(4)
            component1 = hw.Component("compoent1", 2, 3, None)
            aIterationMapo.addComponent(component1, [0, 1, 2])
            self.assertRaises(ValueError, hw.Schedule, aIterationMapo, "hi")
    
    def test003Constructure(self):
            aCalendar = hw.Calendar()
            aCalendar.addDay(80)
            self.assertRaises(ValueError, hw.Schedule, "hi", aCalendar)
            
    def test004GetProjectEndDay(self):
            aIterationMapo = hw.ComponentIterationMap(4)
            component1 = hw.Component("compoent1", 1, 3, None)
            component2 = hw.Component("compoent1", 1, 3, None)
            component3 = hw.Component("compoent1", 1, 3, None)
            component4 = hw.Component("compoent1", 1, 3, None)
            aIterationMapo.addComponent(component1, [3, 1])
            aIterationMapo.addComponent(component2, [0, 4, 0])
            aIterationMapo.addComponent(component3, [0, 2, 2, 1])
            aIterationMapo.addComponent(component4, [0, 0, 0, 7])
            aCalendar = hw.Calendar()
            aCalendar.addDay(10)
            aCalendar.addDay(20)
            aCalendar.addDay(30)
            aCalendar.addDay(40)
            aCalendar.addDay(50)
            aSchedule = hw.Schedule(aIterationMapo, aCalendar)
            self.assertRaises(ValueError, aSchedule.getProjectEndDay, -1)
            endDay = aSchedule.getProjectEndDay(29)
            self.assertEquals(endDay , 2, endDay)
        
    def test005GetIterationPv(self):
            aIterationMapo = hw.ComponentIterationMap(4)
            component1 = hw.Component("compoent1", 1, 3, None)
            component2 = hw.Component("compoent1", 1, 3, None)
            component3 = hw.Component("compoent1", 1, 3, None)
            component4 = hw.Component("compoent1", 1, 3, None)
            aIterationMapo.addComponent(component1, [3, 1])
            aIterationMapo.addComponent(component2, [0, 4, 0])
            aIterationMapo.addComponent(component3, [0, 2, 2, 1])
            aIterationMapo.addComponent(component4, [0, 0, 0, 7])
            aCalendar = hw.Calendar()
            aCalendar.addDay(10)
            aCalendar.addDay(20)
            aCalendar.addDay(30)
            aCalendar.addDay(40)
            aCalendar.addDay(50)
            aSchedule = hw.Schedule(aIterationMapo, aCalendar)
            self.assertRaises(ValueError, aSchedule.getInterationPv, -1)
            self.assertEquals(aSchedule.getInterationPv(1), 3, "3")
            self.assertEquals(aSchedule.getInterationPv(2), 7, "7")
            self.assertEquals(aSchedule.getInterationPv(3), 2, "2")
            self.assertEquals(aSchedule.getInterationPv(4), 8, "8")

    def test006GetIterationEndDay(self):
        aIterationMapo = hw.ComponentIterationMap(4)
        component1 = hw.Component("compoent1", 1, 3, None)
        component2 = hw.Component("compoent1", 1, 3, None)
        component3 = hw.Component("compoent1", 1, 3, None)
        component4 = hw.Component("compoent1", 1, 3, None)
        aIterationMapo.addComponent(component1, [3, 1])
        aIterationMapo.addComponent(component2, [0, 4, 0])
        aIterationMapo.addComponent(component3, [0, 2, 2, 1])
        aIterationMapo.addComponent(component4, [0, 0, 0, 7])
        aCalendar = hw.Calendar()
        aCalendar.addDay(10)
        aCalendar.addDay(20)
        aCalendar.addDay(30)
        aCalendar.addDay(40)
        aCalendar.addDay(50)
        aSchedule = hw.Schedule(aIterationMapo, aCalendar)
        self.assertRaises(ValueError, aSchedule.getIterationEndDay, -1, 1)
        self.assertRaises(ValueError, aSchedule.getIterationEndDay, 1, -1)
        self.assertEquals(aSchedule.getIterationEndDay(100,1), 2, "2")
        self.assertEquals(aSchedule.getIterationEndDay(100,2), 3, "3")
        self.assertEquals(aSchedule.getIterationEndDay(100,3), 3, "4")
        self.assertEquals(aSchedule.getIterationEndDay(100,4), 4, "4")
    
    def test007GetIterationEndDay(self):
        aIterationMapo = hw.ComponentIterationMap(4)
        component1 = hw.Component("compoent1", 1, 3, None)
        component2 = hw.Component("compoent1", 1, 3, None)
        component3 = hw.Component("compoent1", 1, 3, None)
        component4 = hw.Component("compoent1", 1, 3, None)
        aIterationMapo.addComponent(component1, [3, 1])
        aIterationMapo.addComponent(component2, [0, 4, 0])
        aIterationMapo.addComponent(component3, [0, 2, 2, 1])
        aIterationMapo.addComponent(component4, [0, 0, 0, 7])
        aCalendar = hw.Calendar()
        aCalendar.addDay(10)
        aCalendar.addDay(20)
        aCalendar.addDay(30)
        aCalendar.addDay(40)
        aCalendar.addDay(50)
        aSchedule = hw.Schedule(aIterationMapo, aCalendar)
        self.assertRaises(ValueError, aSchedule.getIterationBurndown, -1, 1)
        self.assertRaises(ValueError, aSchedule.getIterationBurndown, 1, -1) 
        self.assertEquals(aSchedule.getIterationBurndown(100, 1), 85, "85")   
        self.assertEquals(aSchedule.getIterationBurndown(100, 2), 50, "50")
        self.assertEquals(aSchedule.getIterationBurndown(100, 3), 40, "40")  
        self.assertEquals(aSchedule.getIterationBurndown(100, 4), 0, "0")  
if __name__ == "__main__":
    import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
