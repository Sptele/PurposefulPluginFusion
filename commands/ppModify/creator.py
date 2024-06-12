import adsk.core
import math
from adsk.core import Point3D

app = adsk.core.Application.get()
ui = app.userInterface

class Creator():
	def __init__(self, data):
		self.data = data

		design = app.activeProduct
		rootComp = design.rootComponent

		trans = adsk.core.Matrix3D.create()
		occ = rootComp.occurrences.addNewComponent(trans)
		occ.component.name = "Your Penis"

		self.shaftComp = occ.component

		sketches = self.shaftComp.sketches
		xyPlane = self.shaftComp.xYConstructionPlane

		self.sketch = sketches.add(xyPlane)

		self.circles = self.sketch.sketchCurves.sketchCircles
		self.extrudes = self.shaftComp.features.extrudeFeatures
		self.lines = self.sketch.sketchCurves.sketchLines
		self.revolves = self.shaftComp.features.revolveFeatures

	def __call__(self):
		shaft = self.shaft()
		self.balls()
		self.tip()
		self.foreskin(shaft)
		self.urethra()
		self.cutBelowAxis()

	def __str__(self):
		return "".join([f"{key}: {self.data[key]}\n" for key in self.data]) if self.data else "No data"

	def shaft(self):
		self.circles.addByCenterRadius(Point3D.create(0,0,0), int(self.data["girth"]) / 20)

		prof = self.sketch.profiles.item(0)

		extInput = self.extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
		extInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(int(self.data["length"]) / 10 - int(self.data["foreskinLength"]) / 10))

		return self.extrudes.add(extInput)

	def balls(self):
		girthRadius = int(self.data["girth"]) / 20
		ballRadius = int(self.data["ballDiameter"]) / 20

		condition = ballRadius < girthRadius

		# If hang together: Tangential Balls
		# If not: 30 60 90 triangle

		# I'm a genius
		hypotenuse = ballRadius + girthRadius
		opposite = ballRadius * (7/8) if condition else (ballRadius + girthRadius) / 2
		adjacent = math.sqrt(hypotenuse**2 - opposite**2) if condition else opposite * math.sqrt(3)

		ballX = opposite # If condition, multiply by 7/8 
		ballY = -adjacent * (7/8) # Multiply by 7/8 to have balls be inside the shaft a little (looks better)
		ballZ = ballRadius * (3/4)

		
		self.right(ballX, ballY, ballZ, ballRadius)
		self.left(ballX, ballY, ballZ, ballRadius)
		
		# for i in range(self.sketch.profiles.count):
		# 	ui.messageBox(f"{i} : {self.sketch.profiles.item(i).areaProperties().area}")



	def left(self, ballX, ballY, ballZ, ballRadius):
		self.circles.addByCenterRadius(Point3D.create(-ballX, ballY, ballZ), ballRadius)

		leftBallLine = self.lines.addByTwoPoints(Point3D.create(-ballX, ballY - ballRadius, ballZ), Point3D.create(-ballX, ballY + ballRadius, ballZ))
		leftBallProf = self.sketch.profiles.item(2)

		revInput = self.revolves.createInput(leftBallProf, leftBallLine, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
		angle = adsk.core.ValueInput.createByReal(-math.pi)
		revInput.setAngleExtent(True, angle)

		self.revolves.add(revInput)


	def right(self, ballX, ballY, ballZ, ballRadius):
		self.circles.addByCenterRadius(Point3D.create(ballX, ballY, ballZ), ballRadius)

		rightBallLine = self.lines.addByTwoPoints(Point3D.create(ballX, ballY - ballRadius, ballZ), Point3D.create(ballX, ballY + ballRadius, ballZ))
		rightBallProf = self.sketch.profiles.item(1)

		revInput = self.revolves.createInput(rightBallProf, rightBallLine, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
		angle = adsk.core.ValueInput.createByReal(math.pi)
		revInput.setAngleExtent(True, angle)

		self.revolves.add(revInput)	

	def tip(self):
		girthRadius = int(self.data["girth"]) / 20
		lengthCM = int(self.data["length"]) / 10

		self.circles.addByCenterRadius(Point3D.create(0, 0, lengthCM), girthRadius)
		line = self.lines.addByTwoPoints(Point3D.create(0, -girthRadius, lengthCM), Point3D.create(0, girthRadius, lengthCM))
		
		prof = self.sketch.profiles.item(0)

		revInput = self.revolves.createInput(prof, line, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
		angle = adsk.core.ValueInput.createByReal(-math.pi)
		revInput.setAngleExtent(True, angle)

		self.revolves.add(revInput)

		line.deleteMe()
	
	def foreskin(self, shaft):
		lengthCM = int(self.data["length"]) / 10
		foreskinLengthCM = int(self.data["foreskinLength"]) / 10
		isCircum = bool(self.data["circumsized"])

		self.circles.addByCenterRadius(Point3D.create(0,0,lengthCM-foreskinLengthCM), (int(self.data["girth"]) / 20) * ((8/7) if not isCircum else (7/8)))

		prof = self.sketch.profiles.item(1)

		extInput = self.extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
		extInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(foreskinLengthCM))

		self.extrudes.add(extInput)

		if isCircum: # Fillet the cut
			edge = shaft.faces.item(0).edges.item(0)
			edgeCollection = adsk.core.ObjectCollection.create()
			edgeCollection.add(edge)
			
			# Create the FilletInput object.
			fillets = self.shaftComp.features.filletFeatures
			filletInput = fillets.createInput()      
			filletInput.addConstantRadiusEdgeSet(edgeCollection, adsk.core.ValueInput.createByReal(0.025), True)

			# Create the fillet.        
			fillets.add(filletInput)

	def urethra(self):
		urethraRadius = int(self.data["urethraDiameter"]) / 20
		girthRadius = int(self.data["girth"]) / 20
		lengthCM = int(self.data["length"]) / 10

		self.circles.addByCenterRadius(Point3D.create(0,-girthRadius/2, lengthCM), urethraRadius)
		prof = self.sketch.profiles.item(1)

		extInput = self.extrudes.createInput(prof, adsk.fusion.FeatureOperations.CutFeatureOperation)
		extInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(girthRadius))

		self.extrudes.add(extInput)

	def cutBelowAxis(self):
		girthDiameter = int(self.data["girth"]) / 10
		ballDiameter = int(self.data["ballDiameter"]) / 10

		total = girthDiameter + ballDiameter

		self.lines.addTwoPointRectangle(Point3D.create(-total, -total, 0), Point3D.create(total, total, 0))

		boxProf = self.sketch.profiles.item(8)
		boxInput = self.extrudes.createInput(boxProf, adsk.fusion.FeatureOperations.CutFeatureOperation)

		#ui.messageBox(f"{boxProf.areaProperties().area}")

		boxInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(-5))

		self.extrudes.add(boxInput)
