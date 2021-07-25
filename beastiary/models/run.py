class Run(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String)
    samples = db.relationship("Sample", backref="runs", lazy=True)
    __tablename__ = "runs"
